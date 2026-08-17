# -*- coding: utf-8 -*-
"""
构建动量因子库
=====================================================================
输入 : INTERN_CODE/data/raw/stock/MktEqudAdjAfGet/*.csv
       (每只股票一个后复权日线 csv, 来自通联 MktEqudAdjAfGet)
输出 : INTERN_CODE/分析结果/factors/
       basic_mom.pkl.gz     基础动量 + 截面分位数 + 截面z-score  (15 个因子)
       rank_mom.pkl.gz      Rank 动量                           (5 个因子)
       smooth_mom.pkl.gz    平滑动量                            (5 个因子)
       position.pkl.gz      价格区间位置                         (5 个因子)
       returns.pkl.gz       收盘价与日收益率
       因子清单.csv         全部因子的公式说明

因子定义(按《动量因子详细描述》):
  窗口 w ∈ {5, 20, 60, 120, 252}
  1) 基础动量 mom_w
     短期(w=5,20) : P_t / P_{t-w} - 1
     长期(w>=60)  : P_{t-20} / P_{t-w} - 1   (跳过最近20个交易日)
  2) mom_rankpct_w : 当日横截面分位数(0~1)
  3) mom_z_w       : 当日横截面 z-score
  4) rankmom_w     : 日收益率横截面排名 -> Wright(2000) 变换 -> w 日平均
  5) smoothmom_w   : w 日累计涨跌幅 / w 日 |日收益率| 之和
  6) position_w    : (P_t - 过去w日最低) / (过去w日最高 - 过去w日最低)

说明:
  * 所有窗口均按"交易日"计, 先按 ticker + tradeDate 排序再滚动.
  * 默认剔除 B 股(200xxx/900xxx), 避免不同币种混进同一横截面.
  * 因子默认存成 gzip 压缩的 pickle; 若环境装了 pyarrow 会自动改用 parquet.
  * 支持 --read-only: 只做"读取+合并+清洗"并缓存面板, 便于分两步跑.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyarrow  # noqa: F401
    FORMAT = "parquet"
except Exception:  # 装不了 pyarrow 时自动退回 pickle
    FORMAT = "pkl"

def _find_project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / "data").is_dir() and (parent / "分析结果").is_dir():
            return parent
    return p.parent


PROJECT_DIR = _find_project_root()
DATA_DIR = PROJECT_DIR / "data" / "raw" / "stock" / "MktEqudAdjAfGet"
OUT_DIR = PROJECT_DIR / "分析结果" / "factors"
PANEL_CACHE = OUT_DIR / "panel.pkl.gz"  # 合并清洗后的面板缓存(断点续跑用)

WINDOWS = [5, 20, 60, 120, 252]
SKIP = 20                # 长期动量跳过最近交易日数
INCLUDE_B_SHARES = False  # 是否把 B 股也纳入因子库

FLOAT = np.float32


def is_a_share(ticker: str) -> bool:
    return not (ticker.startswith("200") or ticker.startswith("900"))


def load_panel() -> pd.DataFrame:
    """读取全部 csv 并合并成一个长面板: tradeDate x ticker x closePrice"""
    if PANEL_CACHE.exists():
        print(f"发现面板缓存, 直接加载: {PANEL_CACHE}")
        return pd.read_pickle(PANEL_CACHE)

    files = sorted(DATA_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"目录下没有 csv: {DATA_DIR}")
    print(f"共 {len(files)} 个 csv, 开始读取 ...")
    frames = []
    for i, f in enumerate(files, 1):
        df = pd.read_csv(
            f,
            usecols=["ticker", "tradeDate", "closePrice"],
            dtype={"ticker": "str"},
            encoding="utf-8-sig",
        )
        frames.append(df)
        if i % 1000 == 0 or i == len(files):
            print(f"   已读取 {i}/{len(files)}")

    panel = pd.concat(frames, ignore_index=True)
    panel["tradeDate"] = pd.to_datetime(panel["tradeDate"])
    panel = panel.drop_duplicates(["ticker", "tradeDate"], keep="last")
    panel = panel.sort_values(["ticker", "tradeDate"], kind="stable").reset_index(drop=True)

    if not INCLUDE_B_SHARES:
        n_before = panel["ticker"].nunique()
        panel = panel[panel["ticker"].map(is_a_share)].reset_index(drop=True)
        print(f"   剔除 B 股后股票数: {n_before} -> {panel['ticker'].nunique()}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_pickle(PANEL_CACHE, compression="gzip")
    print(f"   面板已缓存: {PANEL_CACHE}")
    return panel


def save(df: pd.DataFrame, name: str) -> None:
    ext = "parquet" if FORMAT == "parquet" else "pkl.gz"
    path = OUT_DIR / f"{name}.{ext}"
    if FORMAT == "parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_pickle(path, compression="gzip")
    print(f"   已保存 {path} ({len(df):,} 行 x {len(df.columns)} 列)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true",
                        help="只读取/合并/清洗数据并缓存面板, 不算因子")
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 70)
    print("第 1 步 / 6: 读取并合并全部 csv")
    panel = load_panel()
    n_stock, n_date = panel["ticker"].nunique(), panel["tradeDate"].nunique()
    print(f"   面板规模: {len(panel):,} 行, {n_stock:,} 只股票, {n_date:,} 个交易日, "
          f"{panel['tradeDate'].min().date()} ~ {panel['tradeDate'].max().date()}")
    if args.read_only:
        print("--read-only, 到此为止。")
        return

    print("=" * 70)
    print("第 2 步 / 6: 计算日收益率")
    panel["closePrice"] = panel["closePrice"].astype(FLOAT)
    panel["ret"] = panel.groupby("ticker")["closePrice"].pct_change().astype(FLOAT)

    print("=" * 70)
    print("第 3 步 / 6: 基础动量 (短期点对点 / 长期跳过20天)")
    g_close = panel.groupby("ticker")["closePrice"]
    for w in WINDOWS:
        if w <= 20:
            panel[f"mom_{w}"] = (panel["closePrice"] / g_close.shift(w) - 1).astype(FLOAT)
        else:
            panel[f"mom_{w}"] = (g_close.shift(SKIP) / g_close.shift(w) - 1).astype(FLOAT)

    print("=" * 70)
    print("第 4 步 / 6: 平滑动量与价格区间位置")
    panel["ret_abs"] = panel["ret"].abs()
    for w in WINDOWS:
        num = panel["closePrice"] / g_close.shift(w) - 1
        den = panel.groupby("ticker")["ret_abs"].rolling(w, min_periods=w).sum().reset_index(level=0, drop=True)
        panel[f"smoothmom_{w}"] = (num / den).astype(FLOAT)
        hi = g_close.rolling(w, min_periods=w).max().reset_index(level=0, drop=True)
        lo = g_close.rolling(w, min_periods=w).min().reset_index(level=0, drop=True)
        panel[f"position_{w}"] = ((panel["closePrice"] - lo) / (hi - lo)).astype(FLOAT)
    panel.drop(columns=["ret_abs"], inplace=True)

    print("=" * 70)
    print("第 5 步 / 6: Rank 动量 (日收益排名 -> Wright 变换 -> 窗口平均)")
    g_date_ret = panel.groupby("tradeDate")["ret"]
    daily_rank = g_date_ret.rank(method="average")          # 1..N 升序
    n_daily = g_date_ret.transform("count").astype(FLOAT)   # 当日有效样本数 N
    denom = np.sqrt((n_daily - 1) * (n_daily + 1) / 12.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        wright = (daily_rank - (n_daily + 1) / 2.0) / denom
    panel["daily_rank"] = wright.replace([np.inf, -np.inf], np.nan).astype(FLOAT)
    for w in WINDOWS:
        panel[f"rankmom_{w}"] = (
            panel.groupby("ticker")["daily_rank"]
            .rolling(w, min_periods=w)
            .mean()
            .reset_index(level=0, drop=True)
            .astype(FLOAT)
        )
    panel.drop(columns=["daily_rank"], inplace=True)

    print("=" * 70)
    print("第 6 步 / 6: 基础动量的截面分位数与 z-score")
    for w in WINDOWS:
        col = f"mom_{w}"
        g = panel.groupby("tradeDate")[col]
        panel[f"mom_rankpct_{w}"] = g.rank(pct=True).astype(FLOAT)
        mu = g.transform("mean")
        sd = g.transform(lambda s: s.std(ddof=0))
        panel[f"mom_z_{w}"] = ((panel[col] - mu) / sd).replace([np.inf, -np.inf], np.nan).astype(FLOAT)

    panel = panel.replace([np.inf, -np.inf], np.nan)

    print("=" * 70)
    print("保存因子库 ...")
    keys = ["tradeDate", "ticker"]
    save(panel[keys + [c for c in panel.columns if c.startswith("mom_")]], "basic_mom")
    save(panel[keys + [c for c in panel.columns if c.startswith("rankmom_")]], "rank_mom")
    save(panel[keys + [c for c in panel.columns if c.startswith("smoothmom_")]], "smooth_mom")
    save(panel[keys + [c for c in panel.columns if c.startswith("position_")]], "position")
    save(panel[keys + ["closePrice", "ret"]], "returns")

    manifest = []
    for w in WINDOWS:
        formula = "P_t / P_{t-w} - 1" if w <= 20 else "P_{t-20} / P_{t-w} - 1 (跳过最近20天)"
        manifest.append(["基础动量", f"mom_{w}", w, formula])
        manifest.append(["截面分位数", f"mom_rankpct_{w}", w, "基础动量当日横截面分位数(0~1)"])
        manifest.append(["截面z-score", f"mom_z_{w}", w, "基础动量当日横截面z-score"])
        manifest.append(["Rank动量", f"rankmom_{w}", w, "日收益排名->Wright变换->w日平均"])
        manifest.append(["平滑动量", f"smoothmom_{w}", w, "w日累计涨跌幅 / w日|日收益|之和"])
        manifest.append(["价格区间位置", f"position_{w}", w, "(P_t-min)/(max-min), 过去w日"])
    pd.DataFrame(manifest, columns=["因子族", "因子名", "窗口", "公式"]).to_csv(
        OUT_DIR / "因子清单.csv", index=False, encoding="utf-8-sig")
    print(f"   因子总数: {len(manifest)}")

    print("=" * 70)
    print(f"完成, 用时 {time.time() - t0:.0f} 秒")
    print("\n抽查 000001 最近 3 天:")
    print(panel[panel["ticker"] == "000001"].tail(3).T)


if __name__ == "__main__":
    main()

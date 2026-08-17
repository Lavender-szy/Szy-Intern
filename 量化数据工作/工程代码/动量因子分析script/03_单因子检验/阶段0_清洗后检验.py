# -*- coding: utf-8 -*-
"""
阶段0 清洗后: 重新做单因子检验
=====================================================================
输入 : 因子库 + returns + clean/清洗面板.pkl.gz
输出 : 分析结果/results/清洗后/
       因子检验汇总.csv / 分组收益.csv / IC序列.csv
口径 : 只保留 clean 样本(ST/次新/涨跌停/停牌剔除后), 其余与 单因子检验.py 一致。
      每个因子完成后写 done_factors.txt, 中断后重跑自动跳过。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def _find_project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / "data").is_dir() and (parent / "分析结果").is_dir():
            return parent
    return p.parent


PROJECT_DIR = _find_project_root()
FACTOR_DIR = PROJECT_DIR / "分析结果" / "factors"
CLEAN_PANEL = PROJECT_DIR / "分析结果" / "clean" / "清洗面板.pkl.gz"
OUT_DIR = PROJECT_DIR / "分析结果" / "results" / "清洗后"
DONE_FILE = OUT_DIR / "done_factors.txt"
FACTOR_FILES = ["basic_mom", "rank_mom", "smooth_mom", "position"]
N_GROUPS = 10
ANNUAL_DAYS = 252


def log(msg: str) -> None:
    print(msg, flush=True)


def load(name: str) -> pd.DataFrame:
    pkl = FACTOR_DIR / f"{name}.pkl.gz"
    pq = FACTOR_DIR / f"{name}.parquet"
    if pq.exists():
        return pd.read_parquet(pq)
    return pd.read_pickle(pkl)


def factor_meta(name: str) -> tuple[str, str]:
    fams = [("mom_rankpct_", "截面分位数"), ("mom_z_", "截面z-score"), ("mom_", "基础动量"),
            ("rankmom_", "Rank动量"), ("smoothmom_", "平滑动量"), ("position_", "价格区间位置")]
    for prefix, fam in fams:
        if name.startswith(prefix):
            return fam, name.split("_")[-1]
    return "", ""


def group_ic(x: pd.Series, y: pd.Series, date: pd.Series) -> pd.Series:
    sum_x = x.groupby(date).sum()
    sum_y = y.groupby(date).sum()
    sum_xy = (x * y).groupby(date).sum()
    sum_x2 = (x * x).groupby(date).sum()
    sum_y2 = (y * y).groupby(date).sum()
    n = x.groupby(date).count()
    cov = sum_xy - sum_x * sum_y / n
    varx = sum_x2 - sum_x ** 2 / n
    vary = sum_y2 - sum_y ** 2 / n
    return cov / np.sqrt(varx * vary)


def test_one(df: pd.DataFrame, factor: str,
             r_rank_all: pd.Series) -> tuple[dict | None, pd.DataFrame | None, pd.Series | None]:
    f_rank_all = df.groupby("tradeDate")[factor].rank(pct=True)
    mask = (df[factor].notna() & df["fwd_ret"].notna()).to_numpy()
    date = df["tradeDate"][mask]
    f_rank = f_rank_all[mask]
    r_rank = r_rank_all[mask]
    del f_rank_all
    if len(f_rank) < 1000:
        return None, None, None

    ic = group_ic(f_rank, r_rank, date).dropna()
    if len(ic) < 20:
        return None, None, None
    ic_mean, ic_std = ic.mean(), ic.std(ddof=1)
    icir = ic_mean / ic_std if ic_std and not np.isnan(ic_std) else np.nan
    ic_pos = (ic > 0).mean()
    ic_t = ic_mean / ic_std * np.sqrt(len(ic)) if ic_std else np.nan

    f_rank_ord_all = df.groupby("tradeDate")[factor].rank(method="first")
    n_daily_all = df.groupby("tradeDate")[factor].transform("count")
    grp = np.ceil((f_rank_ord_all / n_daily_all * N_GROUPS).to_numpy()[mask]) \
        .clip(1, N_GROUPS).astype(int)
    dg = pd.DataFrame({"date": date.to_numpy(), "grp": grp,
                       "r": df["fwd_ret"].to_numpy()[mask]})
    gmat = dg.groupby(["date", "grp"])["r"].mean().unstack().reindex(columns=range(1, N_GROUPS + 1))
    gmean = gmat.mean()
    gt = gmean / gmat.std(ddof=1) * np.sqrt(gmat.count())
    ls = gmat[N_GROUPS] - gmat[1]
    ls_mean, ls_t = ls.mean(), ls.mean() / ls.std(ddof=1) * np.sqrt(ls.count())

    fam, window = factor_meta(factor)
    row = {
        "因子名": factor, "因子族": fam, "窗口": window,
        "IC均值": round(float(ic_mean), 5),
        "IC标准差": round(float(ic_std), 5),
        "ICIR": round(float(icir), 4),
        "IC>0占比": round(float(ic_pos), 4),
        "IC_t": round(float(ic_t), 3),
        "多空日收益": round(float(ls_mean), 6),
        "多空年化": round(float(ls_mean * ANNUAL_DAYS), 4),
        "多空_t": round(float(ls_t), 3),
        "检验天数": int(len(ic)),
    }
    group_data = pd.DataFrame({
        "因子名": factor, "组别": range(1, N_GROUPS + 1),
        "组均日收益": [round(v, 6) for v in gmean.fillna(0).tolist()],
        "年化": [round(v * ANNUAL_DAYS, 4) for v in gmean.fillna(0).tolist()],
        "组_t": [round(v, 3) for v in gt.fillna(0).tolist()],
    })
    return row, group_data, ic


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    done = set()
    if DONE_FILE.exists():
        done = set(DONE_FILE.read_text(encoding="utf-8").splitlines())
    if done:
        log(f"跳过已完成的 {len(done)} 个因子")

    log("加载清洗面板 ...")
    clean = pd.read_pickle(CLEAN_PANEL)[["tradeDate", "ticker", "clean"]]

    log("加载 returns ...")
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    ret = ret.merge(clean, on=["tradeDate", "ticker"], how="left")
    ret = ret[ret["clean"] == True]  # noqa: E712
    ret = ret[["tradeDate", "ticker", "ret", "fwd_ret"]].astype({"ret": np.float32, "fwd_ret": np.float32})
    log(f"   清洗后 returns: {len(ret):,} 行")

    summary_rows, group_rows, ic_rows = [], [], []
    for fam in FACTOR_FILES:
        fac = load(fam)
        df = fac.merge(ret, on=["tradeDate", "ticker"], how="inner")
        log(f"   {fam}: {len(df):,} 行")
        r_rank_all = df.groupby("tradeDate")["fwd_ret"].rank(pct=True)
        for factor in [c for c in fac.columns if c not in ("tradeDate", "ticker")]:
            if factor in done:
                continue
            t1 = time.time()
            row, gdf, ic = test_one(df, factor, r_rank_all)
            if row is None:
                log(f"   {factor}: 样本不足, 跳过")
                continue
            summary_rows.append(row)
            group_rows.append(gdf)
            for dt, v in ic.items():
                ic_rows.append([dt.strftime("%Y-%m-%d"), factor, round(float(v), 5)])
            with DONE_FILE.open("a", encoding="utf-8") as f:
                f.write(factor + "\n")
            log(f"   {factor}: IC={row['IC均值']}, ICIR={row['ICIR']}, "
                f"多空_t={row['多空_t']}, 用时 {time.time() - t1:.0f}s")
        del df, fac

    if summary_rows:
        pd.DataFrame(summary_rows).sort_values("ICIR", ascending=False, na_position="last") \
            .to_csv(OUT_DIR / "因子检验汇总.csv", index=False, encoding="utf-8-sig")
        pd.concat(group_rows, ignore_index=True) \
            .to_csv(OUT_DIR / "分组收益.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame(ic_rows, columns=["日期", "因子名", "IC"]) \
            .to_csv(OUT_DIR / "IC序列.csv", index=False, encoding="utf-8-sig")
        log(f"\n结果已保存到 {OUT_DIR}")
        log(pd.DataFrame(summary_rows).sort_values("ICIR", ascending=False).head(12).to_string(index=False))
    log(f"总用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

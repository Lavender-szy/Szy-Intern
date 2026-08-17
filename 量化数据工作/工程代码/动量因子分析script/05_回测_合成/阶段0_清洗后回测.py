# -*- coding: utf-8 -*-
"""
阶段0 清洗后: 月度调仓回测 + 多因子合成
=====================================================================
输入 : 因子库 + returns + clean/清洗面板.pkl.gz + results/清洗后/因子检验汇总.csv
输出 : 分析结果/results/清洗后/
       月度回测_汇总.csv / 月度回测_净值.csv / 综合因子_IC.csv
口径 : 只保留 clean 样本; 方向统一取清洗后 IC 符号; 组合月度等权持有, 未计成本。
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
FACTOR_FILES = ["basic_mom", "rank_mom", "smooth_mom", "position"]

SELECTED = [
    "mom_5", "mom_20", "mom_60", "mom_120", "mom_252",
    "rankmom_120", "rankmom_252",
    "smoothmom_5", "smoothmom_20",
    "position_5", "position_20", "position_60",
]

COMPOSITES = {
    "综合A(反转+趋势)": {
        "factors": ["mom_5", "mom_20", "rankmom_252"],
        "signs": {"mom_5": -1, "mom_20": -1, "rankmom_252": 1},
    },
    "综合B(+位置)": {
        "factors": ["mom_5", "mom_20", "rankmom_252", "position_5"],
        "signs": {"mom_5": -1, "mom_20": -1, "rankmom_252": 1, "position_5": -1},
    },
}


def log(msg: str) -> None:
    print(msg, flush=True)


def load(name: str) -> pd.DataFrame:
    pkl = FACTOR_DIR / f"{name}.pkl.gz"
    pq = FACTOR_DIR / f"{name}.parquet"
    if pq.exists():
        return pd.read_parquet(pq)
    return pd.read_pickle(pkl)


def perf_stats(monthly: pd.Series) -> dict:
    m = monthly.to_numpy(dtype=float)
    m = m[~np.isnan(m)]
    if len(m) < 3:
        return {}
    nav = np.cumprod(1 + m)
    total = nav[-1] - 1
    n = len(m)
    ann = (1 + total) ** (12 / n) - 1
    vol = m.std(ddof=1) * np.sqrt(12)
    sharpe = (m.mean() * 12) / vol if vol > 0 else np.nan
    maxdd = (nav / np.maximum.accumulate(nav) - 1).min()
    return {"年化收益": ann, "年化波动": vol, "夏普": sharpe, "最大回撤": maxdd, "累计收益": total}


def monthly_backtest(F: pd.DataFrame, ret_wide: pd.DataFrame,
                     month_ends: list[pd.Timestamp]) -> tuple[pd.DataFrame, float]:
    N = F.notna().sum(axis=1)
    rank_ord = F.rank(axis=1, method="first")
    grp = np.ceil(rank_ord.div(N, axis=0) * 10).clip(1, 10)
    top_mask = grp == 10
    bot_mask = grp == 1
    rows, members_top = [], []
    for i in range(len(month_ends) - 1):
        t0, t1 = month_ends[i], month_ends[i + 1]
        if t0 not in F.index:
            continue
        top_t = F.columns[top_mask.loc[t0].to_numpy()]
        bot_t = F.columns[bot_mask.loc[t0].to_numpy()]
        if len(top_t) < 20 or len(bot_t) < 20:
            continue
        daily = ret_wide.loc[(ret_wide.index > t0) & (ret_wide.index <= t1)]
        if len(daily) == 0:
            continue
        r_top = (1 + daily[top_t].mean(axis=1)).prod() - 1
        r_bot = (1 + daily[bot_t].mean(axis=1)).prod() - 1
        rows.append({"日期": t1, "组10": r_top, "组1": r_bot})
        members_top.append(set(top_t))
    monthly = pd.DataFrame(rows).set_index("日期")
    turnover = np.nan
    if len(members_top) > 1:
        t = [1 - len(members_top[k] & members_top[k - 1]) / max(len(members_top[k]), 1)
             for k in range(1, len(members_top))]
        turnover = float(np.mean(t))
    return monthly, turnover


def ic_series(F: pd.DataFrame, fwd_rank: pd.DataFrame) -> pd.Series:
    return F.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    log("加载清洗面板 ...")
    clean = pd.read_pickle(CLEAN_PANEL)[["tradeDate", "ticker", "clean"]]

    log("加载因子、收益率 ...")
    frames = [load(n) for n in FACTOR_FILES]
    fac = pd.concat([f.set_index(["tradeDate", "ticker"]) for f in frames], axis=1).reset_index()
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    ret = ret.merge(clean, on=["tradeDate", "ticker"], how="left")
    ret = ret[ret["clean"] == True]  # noqa: E712
    ret = ret[["tradeDate", "ticker", "ret", "fwd_ret"]].astype({"ret": np.float32, "fwd_ret": np.float32})
    df = fac.merge(ret, on=["tradeDate", "ticker"], how="inner")
    log(f"   清洗后面板: {len(df):,} 行, 用时 {time.time() - t0:.0f}s")

    ret_wide = df.pivot(index="tradeDate", columns="ticker", values="ret")
    fwd_rank = df.pivot(index="tradeDate", columns="ticker", values="fwd_ret").rank(axis=1, pct=True)
    all_dates = np.sort(df["tradeDate"].unique())
    month_ends = pd.Series(all_dates).groupby(pd.Series(all_dates).dt.to_period("M")).max().tolist()
    log(f"   交易日 {len(all_dates)}, 月度调仓点 {len(month_ends)}")

    summary_csv = pd.read_csv(OUT_DIR / "因子检验汇总.csv", encoding="utf-8-sig")
    ic_map = dict(zip(summary_csv["因子名"], summary_csv["IC均值"]))

    summary_rows, nav_rows, comp_ic_rows = [], [], []
    for f in SELECTED:
        t1 = time.time()
        F = df.pivot(index="tradeDate", columns="ticker", values=f)
        monthly, turnover = monthly_backtest(F, ret_wide, month_ends)
        if len(monthly) < 3:
            log(f"{f}: 样本不足, 跳过")
            continue
        sign = 1 if ic_map.get(f, 0) >= 0 else -1
        ls_dir = monthly["组10"] - monthly["组1"] if sign == 1 else monthly["组1"] - monthly["组10"]
        st = perf_stats(ls_dir)
        st_hl = perf_stats(monthly["组10"] - monthly["组1"])
        st_lh = perf_stats(monthly["组1"] - monthly["组10"])
        summary_rows.append({
            "因子": f,
            "方向": "高减低" if sign == 1 else "低减高",
            "月数": len(monthly),
            "年化收益": round(st.get("年化收益", np.nan), 4),
            "年化波动": round(st.get("年化波动", np.nan), 4),
            "夏普": round(st.get("夏普", np.nan), 2),
            "最大回撤": round(st.get("最大回撤", np.nan), 4),
            "换手率": round(turnover, 3),
            "累计收益": round(st.get("累计收益", np.nan), 4),
            "高减低年化": round(st_hl.get("年化收益", np.nan), 4),
            "低减高年化": round(st_lh.get("年化收益", np.nan), 4),
        })
        nav = (1 + ls_dir).cumprod()
        for dt, v in nav.items():
            nav_rows.append({"因子": f, "日期": dt.strftime("%Y-%m-%d"), "净值": round(float(v), 6)})
        log(f"   {f}: 方向={'高减低' if sign == 1 else '低减高'}, "
            f"年化={st.get('年化收益', np.nan):.4f}, 夏普={st.get('夏普', np.nan):.2f}, "
            f"回撤={st.get('最大回撤', np.nan):.4f}, 换手={turnover:.3f}, 用时 {time.time() - t1:.0f}s")
        del F

    for name, cfg in COMPOSITES.items():
        t1 = time.time()
        parts, counts = None, None
        for f in cfg["factors"]:
            F = df.pivot(index="tradeDate", columns="ticker", values=f)
            directed = (F.rank(axis=1, pct=True) - 0.5) * cfg["signs"][f]
            parts = directed if parts is None else parts.add(directed, fill_value=0)
            cnt = directed.notna().astype(np.float32)
            counts = cnt if counts is None else counts.add(cnt, fill_value=0)
            del F
        comp = parts / counts
        ic = ic_series(comp, fwd_rank)
        m, s = ic.mean(), ic.std(ddof=1)
        monthly, turnover = monthly_backtest(comp, ret_wide, month_ends)
        st = perf_stats(monthly["组10"] - monthly["组1"])
        comp_ic_rows.append({
            "合成因子": name,
            "IC均值": round(float(m), 5),
            "ICIR": round(float(m / s), 4) if s and not np.isnan(s) else np.nan,
            "IC_t": round(float(m / s * np.sqrt(len(ic))), 3) if s and not np.isnan(s) else np.nan,
            "月数": len(monthly),
            "年化收益": round(st.get("年化收益", np.nan), 4),
            "夏普": round(st.get("夏普", np.nan), 2),
            "最大回撤": round(st.get("最大回撤", np.nan), 4),
            "换手率": round(turnover, 3),
            "月均组10收益": round(float(monthly["组10"].mean()), 5),
            "月均组1收益": round(float(monthly["组1"].mean()), 5),
        })
        nav = (1 + monthly["组10"] - monthly["组1"]).cumprod()
        for dt, v in nav.items():
            nav_rows.append({"因子": name, "日期": dt.strftime("%Y-%m-%d"), "净值": round(float(v), 6)})
        log(f"   {name}: IC={m:+.5f}, ICIR={m / s:.3f}, 年化={st.get('年化收益', np.nan):.4f}, "
            f"夏普={st.get('夏普', np.nan):.2f}, 回撤={st.get('最大回撤', np.nan):.4f}, "
            f"用时 {time.time() - t1:.0f}s")
        del comp

    pd.DataFrame(summary_rows).sort_values("夏普", ascending=False) \
        .to_csv(OUT_DIR / "月度回测_汇总.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(nav_rows).to_csv(OUT_DIR / "月度回测_净值.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(comp_ic_rows).to_csv(OUT_DIR / "综合因子_IC.csv", index=False, encoding="utf-8-sig")

    log("\n清洗后月度回测(按夏普排序):")
    log(pd.DataFrame(summary_rows).sort_values("夏普", ascending=False).head(12).to_string(index=False))
    log("\n清洗后综合因子:")
    log(pd.DataFrame(comp_ic_rows).to_string(index=False))
    log(f"\n完成, 总用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

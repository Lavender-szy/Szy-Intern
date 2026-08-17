# -*- coding: utf-8 -*-
"""
市值分层检验 + T+1 成交精细化回测
=====================================================================
输入 : 因子库 + returns + 市值面板 + 清洗面板
输出 : 分析结果/results/清洗后/
       市值分层_IC.csv        全市场/小/中/大市值 内的因子 IC
       市值分层_月度多空.csv  各市值分层内的月度十分位多空绩效
       T1回测对比.csv         收盘成交 vs T+1收盘成交(跳过调仓次日) 的毛/净绩效

口径:
  * 市值分层: 每个交易日按 log(总市值) 横截面三分位(小/中/大);
  * T+1 成交: 假设在调仓日次日收盘买入, 组合收益跳过调仓后第一个交易日;
  * 成本: 换手 x 单边成本(0.15%) x 2。
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
    "综合A(反转+趋势)": {"factors": ["mom_5", "mom_20", "rankmom_252"],
                      "signs": {"mom_5": -1, "mom_20": -1, "rankmom_252": 1}},
    "综合B(+位置)": {"factors": ["mom_5", "mom_20", "rankmom_252", "position_5"],
                   "signs": {"mom_5": -1, "mom_20": -1, "rankmom_252": 1, "position_5": -1}},
}
ONE_WAY = 0.0015
BUCKETS = [("全市场", None), ("小市值", 1), ("中市值", 2), ("大市值", 3)]


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
    return {"年化收益": ann, "夏普": sharpe, "最大回撤": maxdd, "累计收益": total}


def monthly_backtest(F: pd.DataFrame, ret_wide: pd.DataFrame, month_ends: list,
                     skip_first_day: bool = False) -> tuple[pd.DataFrame, list[float]]:
    N = F.notna().sum(axis=1)
    rank_ord = F.rank(axis=1, method="first")
    grp = np.ceil(rank_ord.div(N, axis=0) * 10).clip(1, 10)
    top_mask = grp == 10
    bot_mask = grp == 1
    rows, turns, prev_top = [], [], None
    for i in range(len(month_ends) - 1):
        t0, t1 = month_ends[i], month_ends[i + 1]
        if t0 not in F.index:
            continue
        top_t = F.columns[top_mask.loc[t0].to_numpy()]
        bot_t = F.columns[bot_mask.loc[t0].to_numpy()]
        if len(top_t) < 20 or len(bot_t) < 20:
            continue
        daily = ret_wide.loc[(ret_wide.index > t0) & (ret_wide.index <= t1)]
        if skip_first_day and len(daily) > 0:
            daily = daily.iloc[1:]
        if len(daily) == 0:
            continue
        r_top = (1 + daily[top_t].mean(axis=1)).prod() - 1
        r_bot = (1 + daily[bot_t].mean(axis=1)).prod() - 1
        tt = 1 - len(set(top_t) & (prev_top or set())) / max(len(top_t), 1) if prev_top is not None else 1.0
        rows.append({"日期": t1, "组10": r_top, "组1": r_bot})
        turns.append(tt)
        prev_top = set(top_t)
    monthly = pd.DataFrame(rows).set_index("日期")
    return monthly, turns


def ic_series(F: pd.DataFrame, fwd_rank: pd.DataFrame) -> pd.Series:
    return F.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    log("加载清洗面板、市值、因子、收益率 ...")
    clean = pd.read_pickle(CLEAN_PANEL)[["tradeDate", "ticker", "clean"]]
    mcap = load("market_cap")
    frames = [load(n) for n in FACTOR_FILES]
    fac = pd.concat([f.set_index(["tradeDate", "ticker"]) for f in frames], axis=1).reset_index()
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    ret = ret.merge(clean, on=["tradeDate", "ticker"], how="left")
    ret = ret[ret["clean"] == True]  # noqa: E712
    ret = ret[["tradeDate", "ticker", "ret", "fwd_ret"]].astype({"ret": np.float32, "fwd_ret": np.float32})
    df = fac.merge(ret, on=["tradeDate", "ticker"], how="inner").merge(mcap, on=["tradeDate", "ticker"], how="left")
    df["logmv"] = np.log(df["marketValue"].replace(0, np.nan)).astype(np.float32)
    log(f"   清洗后面板: {len(df):,} 行, 用时 {time.time() - t0:.0f}s")

    ret_wide = df.pivot(index="tradeDate", columns="ticker", values="ret")
    fwd_rank = df.pivot(index="tradeDate", columns="ticker", values="fwd_ret").rank(axis=1, pct=True)
    # 市值三分位
    mv_rank = df.groupby("tradeDate")["logmv"].rank(method="first")
    mv_n = df.groupby("tradeDate")["logmv"].transform("count")
    bucket_long = np.ceil(mv_rank / mv_n * 3).clip(1, 3)
    bucket_wide = df[["tradeDate", "ticker"]].copy()
    bucket_wide["bucket"] = bucket_long
    bucket_wide = bucket_wide.pivot(index="tradeDate", columns="ticker", values="bucket")
    bucket_masks = {1: bucket_wide == 1, 2: bucket_wide == 2, 3: bucket_wide == 3}

    all_dates = np.sort(df["tradeDate"].unique())
    month_ends = pd.Series(all_dates).groupby(pd.Series(all_dates).dt.to_period("M")).max().tolist()

    # 方向: 复用清洗后回测的方向(全样本IC符号)
    prev = pd.read_csv(OUT_DIR / "月度回测_汇总.csv", encoding="utf-8-sig")
    sign_map = {r["因子"]: (1 if r["方向"] == "高减低" else -1) for _, r in prev.iterrows()}

    wide_cache: dict[str, pd.DataFrame] = {}

    def get_wide(f: str) -> pd.DataFrame:
        if f not in wide_cache:
            wide_cache[f] = df.pivot(index="tradeDate", columns="ticker", values=f)
        return wide_cache[f]

    targets = list(SELECTED) + list(COMPOSITES.keys())
    ic_rows, ls_rows, t1_rows = [], [], []

    for label in targets:
        t1 = time.time()
        if label in COMPOSITES:
            cfg = COMPOSITES[label]
            parts, counts = None, None
            for f in cfg["factors"]:
                Ff = get_wide(f)
                directed = (Ff.rank(axis=1, pct=True) - 0.5) * cfg["signs"][f]
                parts = directed if parts is None else parts.add(directed, fill_value=0)
                cnt = directed.notna().astype(np.float32)
                counts = cnt if counts is None else counts.add(cnt, fill_value=0)
            F = parts / counts
            wide_cache[label] = F
        else:
            F = get_wide(label)
        sign = sign_map.get(label, 1)
        dir_name = "高减低" if sign == 1 else "低减高"

        for bname, bnum in BUCKETS:
            bmask = None if bnum is None else bucket_masks[bnum]
            if bmask is not None:
                if not F.index.equals(bmask.index) or not F.columns.equals(bmask.columns):
                    print(f"   形状差异 {label} {bname}: F={F.shape}, mask={bmask.shape}", flush=True)
                bmask = bmask.reindex(index=F.index, columns=F.columns)
            Fb = F if bmask is None else F.where(bmask)
            rr = fwd_rank if bmask is None else fwd_rank.where(bmask).rank(axis=1, pct=True)
            ic = ic_series(Fb, rr)
            m, s = ic.mean(), ic.std(ddof=1)
            ic_rows.append({
                "因子": label, "市值分层": bname,
                "IC均值": round(float(m), 5),
                "ICIR": round(float(m / s), 4) if s and not np.isnan(s) else np.nan,
                "IC_t": round(float(m / s * np.sqrt(len(ic))), 3) if s and not np.isnan(s) else np.nan,
                "天数": int(len(ic)),
            })
            monthly, turns = monthly_backtest(Fb, ret_wide, month_ends)
            if len(monthly) >= 10:
                ls = monthly["组10"] - monthly["组1"] if sign == 1 else monthly["组1"] - monthly["组10"]
                st = perf_stats(ls)
                ls_rows.append({
                    "因子": label, "市值分层": bname, "方向": dir_name,
                    "年化_毛": round(st.get("年化收益", np.nan), 4),
                    "夏普_毛": round(st.get("夏普", np.nan), 2),
                    "最大回撤": round(st.get("最大回撤", np.nan), 4),
                    "换手率": round(float(np.mean(turns)), 3) if turns else np.nan,
                    "月数": len(monthly),
                })

        # T+1 对比(全市场)
        m_close, turns_close = monthly_backtest(F, ret_wide, month_ends)
        m_t1, turns_t1 = monthly_backtest(F, ret_wide, month_ends, skip_first_day=True)
        for mode, mm, tt in [("收盘成交", m_close, turns_close), ("T+1收盘成交", m_t1, turns_t1)]:
            ls = mm["组10"] - mm["组1"] if sign == 1 else mm["组1"] - mm["组10"]
            cost = pd.Series(tt, index=mm.index) * 2 * ONE_WAY
            st_g = perf_stats(ls)
            st_n = perf_stats(ls - cost)
            t1_rows.append({
                "因子": label, "成交方式": mode, "方向": dir_name,
                "年化_毛": round(st_g.get("年化收益", np.nan), 4),
                "夏普_毛": round(st_g.get("夏普", np.nan), 2),
                "年化_净(0.15%)": round(st_n.get("年化收益", np.nan), 4),
                "夏普_净(0.15%)": round(st_n.get("夏普", np.nan), 2),
                "月数": len(mm),
            })
        log(f"   {label} 完成, 用时 {time.time() - t1:.0f}s")

    pd.DataFrame(ic_rows).to_csv(OUT_DIR / "市值分层_IC.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(ls_rows).to_csv(OUT_DIR / "市值分层_月度多空.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(t1_rows).to_csv(OUT_DIR / "T1回测对比.csv", index=False, encoding="utf-8-sig")
    log(f"完成, 总用时 {time.time() - t0:.0f}s")
    log("\n市值分层 IC(前 20):")
    log(pd.DataFrame(ic_rows).head(20).to_string(index=False))


if __name__ == "__main__":
    main()

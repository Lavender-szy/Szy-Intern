# -*- coding: utf-8 -*-
"""
扣成本月度回测 + 样本外验证
=====================================================================
输入 : 因子库 + returns + 清洗面板
输出 : 分析结果/results/清洗后/
       含成本回测_汇总.csv    单边成本 0.15% 的净绩效 + 0.05%/0.30% 敏感性
       样本外验证.csv         前60%月份定方向, 后40%月份评估

成本口径: 每次调仓, 换手比例 x 单边成本 x 2(卖出+买入); 默认单边 0.15%。
样本外口径: 用前 60% 月份(样本内)的 IC 符号定方向, 在后 40% 月份上评估多空组合。
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

ONE_WAY_COSTS = [0.0005, 0.0015, 0.0030]  # 单边成本敏感性: 0.05% / 0.15% / 0.30%


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
                     ) -> tuple[pd.DataFrame, list[float], list[float]]:
    N = F.notna().sum(axis=1)
    rank_ord = F.rank(axis=1, method="first")
    grp = np.ceil(rank_ord.div(N, axis=0) * 10).clip(1, 10)
    top_mask = grp == 10
    bot_mask = grp == 1
    rows, turn_top, turn_bot, prev_top = [], [], [], None
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
        tt = 1 - len(set(top_t) & (prev_top or set())) / max(len(top_t), 1) if prev_top is not None else 1.0
        rows.append({"日期": t1, "组10": r_top, "组1": r_bot, "换手_多": tt, "换手_空": tt})
        turn_top.append(tt)
        turn_bot.append(tt)
        prev_top = set(top_t)
    monthly = pd.DataFrame(rows).set_index("日期")
    return monthly, turn_top, turn_bot


def ic_series(F: pd.DataFrame, fwd_rank: pd.DataFrame, dates: pd.Index | None = None) -> pd.Series:
    if dates is not None:
        F = F.loc[F.index.isin(dates)]
        fwd_rank = fwd_rank.loc[fwd_rank.index.isin(dates)]
    return F.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    log("加载清洗面板、因子、收益率 ...")
    clean = pd.read_pickle(CLEAN_PANEL)[["tradeDate", "ticker", "clean"]]
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
    n_is = max(int(len(month_ends) * 0.6), 12)
    is_dates = set(month_ends[:n_is])
    oos_ends = month_ends[n_is:]
    log(f"   月度调仓点 {len(month_ends)}: 样本内 {n_is} 个, 样本外 {len(oos_ends)} 个")

    # 因子名 -> 宽表 缓存
    wide_cache: dict[str, pd.DataFrame] = {}

    def get_wide(f: str) -> pd.DataFrame:
        if f not in wide_cache:
            wide_cache[f] = df.pivot(index="tradeDate", columns="ticker", values=f)
        return wide_cache[f]

    cost_rows, oos_rows = [], []
    items = [(f, None) for f in SELECTED] + [(name, cfg) for name, cfg in COMPOSITES.items()]

    for label, cfg in items:
        t1 = time.time()
        if cfg is None:  # 单因子
            F = get_wide(label)
            sign = 1 if ic_series(F, fwd_rank, pd.Index(is_dates)).mean() >= 0 else -1
        else:  # 合成
            parts, counts = None, None
            for f in cfg["factors"]:
                Ff = get_wide(f)
                directed = (Ff.rank(axis=1, pct=True) - 0.5) * cfg["signs"][f]
                parts = directed if parts is None else parts.add(directed, fill_value=0)
                cnt = directed.notna().astype(np.float32)
                counts = cnt if counts is None else counts.add(cnt, fill_value=0)
            F = parts / counts
            wide_cache[label] = F
            sign = 1 if ic_series(F, fwd_rank, pd.Index(is_dates)).mean() >= 0 else -1

        monthly, turn_top, turn_bot = monthly_backtest(F, ret_wide, month_ends)
        if len(monthly) < 10:
            log(f"   {label}: 样本不足, 跳过")
            continue

        # 全样本含成本
        gross = monthly["组10"] - monthly["组1"] if sign == 1 else monthly["组1"] - monthly["组10"]
        cost = (pd.Series(turn_top, index=monthly.index) + pd.Series(turn_bot, index=monthly.index)) / 2 * 2 * ONE_WAY_COSTS[1]
        net = gross - cost
        st_g = perf_stats(gross)
        st_n = perf_stats(net)
        net_sens = {c: perf_stats(gross - cost * (c / ONE_WAY_COSTS[1])) for c in ONE_WAY_COSTS}
        cost_rows.append({
            "因子": label, "方向": "高减低" if sign == 1 else "低减高",
            "年化_毛": round(st_g.get("年化收益", np.nan), 4),
            "夏普_毛": round(st_g.get("夏普", np.nan), 2),
            "年化_净(0.15%)": round(st_n.get("年化收益", np.nan), 4),
            "夏普_净(0.15%)": round(st_n.get("夏普", np.nan), 2),
            "年化_净(0.05%)": round(net_sens[0.0005].get("年化收益", np.nan), 4),
            "年化_净(0.30%)": round(net_sens[0.0030].get("年化收益", np.nan), 4),
            "月均成本": round(float(cost.mean()), 5),
            "月数": len(monthly),
        })

        # 样本外
        oos_monthly = monthly.loc[monthly.index.isin(oos_ends)]
        oos_ls = oos_monthly["组10"] - oos_monthly["组1"] if sign == 1 else oos_monthly["组1"] - oos_monthly["组10"]
        st_o = perf_stats(oos_ls)
        ic_is = ic_series(F, fwd_rank, pd.Index(is_dates)).mean()
        ic_oos = ic_series(F, fwd_rank, monthly.index[monthly.index.isin(oos_ends)]).mean()
        oos_rows.append({
            "因子": label,
            "方向(样本内定)": "高减低" if sign == 1 else "低减高",
            "样本内IC": round(float(ic_is), 5),
            "样本外IC": round(float(ic_oos), 5),
            "样本外年化": round(st_o.get("年化收益", np.nan), 4),
            "样本外夏普": round(st_o.get("夏普", np.nan), 2),
            "样本外最大回撤": round(st_o.get("最大回撤", np.nan), 4),
            "样本外月数": int(len(oos_ls)),
        })
        log(f"   {label}: 方向={'高减低' if sign == 1 else '低减高'}, "
            f"净年化(0.15%)={st_n.get('年化收益', np.nan):.4f}, "
            f"样本外年化={st_o.get('年化收益', np.nan):.4f}, 用时 {time.time() - t1:.0f}s")

    pd.DataFrame(cost_rows).sort_values("夏普_净(0.15%)", ascending=False) \
        .to_csv(OUT_DIR / "含成本回测_汇总.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(oos_rows).sort_values("样本外夏普", ascending=False) \
        .to_csv(OUT_DIR / "样本外验证.csv", index=False, encoding="utf-8-sig")
    log(f"\n完成, 总用时 {time.time() - t0:.0f}s")
    log(pd.DataFrame(cost_rows).sort_values("夏普_净(0.15%)", ascending=False).head(10).to_string(index=False))


if __name__ == "__main__":
    main()

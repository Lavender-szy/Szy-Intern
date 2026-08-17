# -*- coding: utf-8 -*-
"""
第二阶段 A: 因子相关性分析 + 市值中性化检验
=====================================================================
输入 : 分析结果/factors/ 下的因子库、收益率、市值面板
输出 : 分析结果/results/
       因子相关性矩阵.csv     30x30 平均横截面 Spearman 相关(每20个交易日采样)
       高相关因子对.csv       按 |相关系数| 排序的因子对(用于识别冗余)
       市值中性化对比.csv     每个因子中性化前后的 IC/ICIR/IC_t

市值中性化口径:
  每个交易日, 对 log(总市值) 做横截面回归 factor ~ log(mktcap), 取残差作为中性化因子;
  再用残差与 t+1 收益算 RankIC。
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
RESULT_DIR = PROJECT_DIR / "分析结果" / "results"
FACTOR_FILES = ["basic_mom", "rank_mom", "smooth_mom", "position"]
SAMPLE_STEP = 20  # 相关性矩阵每 20 个交易日采一天


def log(msg: str) -> None:
    print(msg, flush=True)


def load(name: str) -> pd.DataFrame:
    pkl = FACTOR_DIR / f"{name}.pkl.gz"
    pq = FACTOR_DIR / f"{name}.parquet"
    if pq.exists():
        return pd.read_parquet(pq)
    return pd.read_pickle(pkl)


def ic_stats(ic: pd.Series) -> tuple[float, float, float]:
    ic = ic.dropna()
    if len(ic) < 20:
        return np.nan, np.nan, np.nan
    m, s = ic.mean(), ic.std(ddof=1)
    if s and not np.isnan(s):
        return float(m), float(s), float(m / s * np.sqrt(len(ic)))
    return float(m), float(s), np.nan


def main() -> None:
    t0 = time.time()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    log("加载因子、收益率、市值面板 ...")
    frames = [load(n) for n in FACTOR_FILES]
    fac = pd.concat([f.set_index(["tradeDate", "ticker"]) for f in frames], axis=1).reset_index()
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    mcap = load("market_cap")
    df = fac.merge(ret[["tradeDate", "ticker", "ret", "fwd_ret"]], on=["tradeDate", "ticker"], how="left")
    df = df.merge(mcap, on=["tradeDate", "ticker"], how="left")
    for c in ["ret", "fwd_ret", "marketValue", "negMarketValue"]:
        df[c] = df[c].astype(np.float32)
    log(f"   面板: {len(df):,} 行, 用时 {time.time() - t0:.0f}s")

    factor_cols = [c for c in fac.columns if c not in ("tradeDate", "ticker")]
    log(f"因子数量: {len(factor_cols)}")

    # ---------------- 1. 因子相关性矩阵 ----------------
    log("第 1 部分: 因子相关性矩阵(横截面 Spearman, 每20个交易日采样)")
    all_dates = np.sort(df["tradeDate"].unique())
    sample_dates = all_dates[::SAMPLE_STEP]
    corr_sum = np.zeros((len(factor_cols), len(factor_cols)))
    corr_cnt = 0
    for d in sample_dates:
        sub = df.loc[df["tradeDate"] == d, factor_cols]
        if len(sub) < 100:
            continue
        r = sub.rank()  # 列内排名, 之后 Pearson 即 Spearman
        c = r.corr().to_numpy(dtype=np.float64)
        corr_sum += np.nan_to_num(c)
        corr_cnt += 1
    corr = corr_sum / max(corr_cnt, 1)
    corr_df = pd.DataFrame(corr, index=factor_cols, columns=factor_cols)
    corr_df.to_csv(RESULT_DIR / "因子相关性矩阵.csv", encoding="utf-8-sig")
    log(f"   采样天数: {corr_cnt}, 已保存 因子相关性矩阵.csv")

    pairs = []
    for i in range(len(factor_cols)):
        for j in range(i + 1, len(factor_cols)):
            pairs.append((factor_cols[i], factor_cols[j], corr[i, j]))
    pairs = pd.DataFrame(pairs, columns=["因子A", "因子B", "相关系数"])
    pairs["|相关系数|"] = pairs["相关系数"].abs()
    pairs = pairs.sort_values("|相关系数|", ascending=False)
    pairs.to_csv(RESULT_DIR / "高相关因子对.csv", index=False, encoding="utf-8-sig")
    log("   已保存 高相关因子对.csv")

    # ---------------- 2. 市值中性化对比 ----------------
    log("第 2 部分: 市值中性化(每个交易日对 log 市值回归取残差)")
    df["logmv"] = np.log(df["marketValue"].replace(0, np.nan))
    logmv_wide = df.pivot(index="tradeDate", columns="ticker", values="logmv")
    fwd_wide = df.pivot(index="tradeDate", columns="ticker", values="fwd_ret")
    fwd_rank = fwd_wide.rank(axis=1, pct=True)

    X = logmv_wide
    n = X.notna().sum(axis=1)
    sx = X.sum(axis=1)
    sx2 = (X * X).sum(axis=1)

    rows = []
    for k, f in enumerate(factor_cols, 1):
        t1 = time.time()
        F = df.pivot(index="tradeDate", columns="ticker", values=f)
        # 原始 IC
        ic_raw = F.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()
        m_raw, s_raw, t_raw = ic_stats(ic_raw)
        # 回归取残差
        sF = F.sum(axis=1)
        sXF = (X * F).sum(axis=1)
        b = (sXF - sx * sF / n) / (sx2 - sx ** 2 / n)
        a = sF / n - b * sx / n
        resid = F.sub(a, axis=0) - X.mul(b, axis=0)
        ic_neu = resid.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()
        m_neu, s_neu, t_neu = ic_stats(ic_neu)
        rows.append({
            "因子名": f,
            "IC_原始": round(m_raw, 5), "ICIR_原始": round(m_raw / s_raw, 4) if s_raw and not np.isnan(s_raw) else np.nan,
            "IC_t_原始": round(t_raw, 3),
            "IC_中性化": round(m_neu, 5), "ICIR_中性化": round(m_neu / s_neu, 4) if s_neu and not np.isnan(s_neu) else np.nan,
            "IC_t_中性化": round(t_neu, 3),
            "检验天数": int(len(ic_neu)),
        })
        log(f"   {f}: IC {m_raw:+.5f} -> {m_neu:+.5f}, 用时 {time.time() - t1:.0f}s")
        del F, resid

    summary = pd.DataFrame(rows).sort_values("IC_t_中性化", ascending=False)
    summary.to_csv(RESULT_DIR / "市值中性化对比.csv", index=False, encoding="utf-8-sig")
    log(f"   已保存 市值中性化对比.csv, 总用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

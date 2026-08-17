# -*- coding: utf-8 -*-
"""
行业分类取数 + 行业/市值中性化(待网关可用时运行)
=====================================================================
说明: 本脚本需要能连通通联数据网关(Tailscale + client.py)。
     网关不可用时, 只会在提示后退出, 不会影响其它分析。

步骤:
  1) DataAPI.EquIndustryGet(industryType="SW2014") 拉全市场行业分类,
     按 ticker 取最新生效记录, 保存到 分析结果/factors/industry.pkl.gz;
  2) 对每个因子做横截面回归 factor ~ log(市值) + 行业虚拟变量, 取残差,
     重算 RankIC, 与"仅市值中性化"对比;
输出: 分析结果/results/行业中性化对比.csv
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
INDUSTRY_FILE = FACTOR_DIR / "industry.pkl.gz"
FACTOR_FILES = ["basic_mom", "rank_mom", "smooth_mom", "position"]


def log(msg: str) -> None:
    print(msg, flush=True)


def load(name: str) -> pd.DataFrame:
    pkl = FACTOR_DIR / f"{name}.pkl.gz"
    pq = FACTOR_DIR / f"{name}.parquet"
    if pq.exists():
        return pd.read_parquet(pq)
    return pd.read_pickle(pkl)


def fetch_industry() -> pd.DataFrame:
    import sys as _sys
    _sys.path.insert(0, str(PROJECT_DIR))
    import client  # noqa: F401

    log("连接网关, 拉取申万一级行业分类 ...")
    df = client.DataAPI.EquIndustryGet(
        industryType="SW2014",
        industry="",
        ticker="",
        secID="",
        field="",
        pandas="1",
    )
    log(f"   返回 {len(df)} 行, 列: {list(df.columns)}")
    # 按 ticker 取最新生效记录
    df = df.sort_values("effectiveDate", ascending=True)
    ind = df.groupby("ticker").tail(1)[["ticker", "industry"]].drop_duplicates("ticker")
    ind.columns = ["ticker", "industry"]
    FACTOR_DIR.mkdir(parents=True, exist_ok=True)
    ind.to_pickle(INDUSTRY_FILE, compression="gzip")
    log(f"   已保存 {INDUSTRY_FILE}, 行业数: {ind['industry'].nunique()}")
    return ind


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

    if not INDUSTRY_FILE.exists():
        try:
            fetch_industry()
        except Exception as e:
            log(f"取数失败({e!r}); 请确认 Tailscale 已连接且在工作日 7:20-23:00 运行。")
            log("行业中性化跳过, 不影响其它分析。")
            return

    log("加载行业、市值、因子与收益率 ...")
    ind = pd.read_pickle(INDUSTRY_FILE)
    frames = [load(n) for n in FACTOR_FILES]
    fac = pd.concat([f.set_index(["tradeDate", "ticker"]) for f in frames], axis=1).reset_index()
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    mcap = load("market_cap")
    df = fac.merge(ret[["tradeDate", "ticker", "ret", "fwd_ret"]], on=["tradeDate", "ticker"], how="left")
    df = df.merge(mcap, on=["tradeDate", "ticker"], how="left")
    df = df.merge(ind, on="ticker", how="left")
    df["logmv"] = np.log(df["marketValue"].replace(0, np.nan))
    log(f"   面板 {len(df):,} 行, 行业覆盖 {df['industry'].notna().mean():.2%}")

    factor_cols = [c for c in fac.columns if c not in ("tradeDate", "ticker")]
    fwd_rank = df.pivot(index="tradeDate", columns="ticker", values="fwd_ret").rank(axis=1, pct=True)
    X = df.pivot(index="tradeDate", columns="ticker", values="logmv")
    n = X.notna().sum(axis=1)
    sx = X.sum(axis=1)
    sx2 = (X * X).sum(axis=1)

    rows = []
    for f in factor_cols:
        F = df.pivot(index="tradeDate", columns="ticker", values=f)
        ic_raw = F.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()
        m_raw, _, t_raw = ic_stats(ic_raw)
        # 市值中性化
        sF = F.sum(axis=1)
        sXF = (X * F).sum(axis=1)
        b = (sXF - sx * sF / n) / (sx2 - sx ** 2 / n)
        a = sF / n - b * sx / n
        resid_size = F.sub(a, axis=0) - X.mul(b, axis=0)
        ic_size = resid_size.rank(axis=1, pct=True).corrwith(fwd_rank, axis=1).dropna()
        m_size, _, t_size = ic_stats(ic_size)
        # 市值 + 行业中性化: 用 groupby 逐日回归(行业哑变量), 仅在有效样本上
        ic_ind = pd.Series(dtype=float)
        valid = df[["tradeDate", "ticker", "logmv", "industry", f]].dropna()
        for dt, g in valid.groupby("tradeDate"):
            y = g[f].to_numpy()
            xx = np.column_stack([np.ones(len(g)), g["logmv"].to_numpy()] +
                                 [pd.get_dummies(g["industry"]).to_numpy()])
            if xx.shape[1] >= len(xx):
                continue
            beta, *_ = np.linalg.lstsq(xx, y, rcond=None)
            resid = y - xx @ beta
            fr = pd.Series(resid).rank(pct=True)
            rr = g["fwd_ret"].rank(pct=True).to_numpy()
            ok = ~(fr.isna().to_numpy() | np.isnan(rr))
            if ok.sum() > 5:
                ic_ind.loc[dt] = np.corrcoef(fr.to_numpy()[ok], rr[ok])[0, 1]
        ic_ind = ic_ind.dropna()
        m_ind, _, t_ind = ic_stats(ic_ind)
        rows.append({
            "因子名": f,
            "IC_原始": round(m_raw, 5), "IC_t_原始": round(t_raw, 3),
            "IC_市值": round(m_size, 5), "IC_t_市值": round(t_size, 3),
            "IC_市值行业": round(m_ind, 5) if not np.isnan(m_ind) else np.nan,
            "IC_t_市值行业": round(t_ind, 3) if not np.isnan(t_ind) else np.nan,
        })
        log(f"   {f}: {m_raw:+.5f} -> 市值 {m_size:+.5f} -> 市值+行业 {m_ind:+.5f}")
        del F

    pd.DataFrame(rows).to_csv(RESULT_DIR / "行业中性化对比.csv", index=False, encoding="utf-8-sig")
    log(f"已保存 行业中性化对比.csv, 总用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

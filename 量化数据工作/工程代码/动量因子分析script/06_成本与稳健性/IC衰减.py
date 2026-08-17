# -*- coding: utf-8 -*-
"""
IC 衰减曲线: 因子对未来 1/5/10/20 个交易日收益的预测能力
=====================================================================
输入 : 因子库 + returns + 清洗面板
输出 : 分析结果/results/清洗后/IC衰减.csv
口径 : 清洗样本; h 日前瞻收益 = close_{t+h}/close_t - 1;
      每交易日因子值与 h 日收益的横截面 Spearman 相关, 对时间取平均。
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
HORIZONS = [1, 5, 10, 20]

FACTORS = ["mom_5", "mom_20", "smoothmom_20", "rankmom_252", "position_20"]
COMPOSITE_A = {"factors": ["mom_5", "mom_20", "rankmom_252"],
               "signs": {"mom_5": -1, "mom_20": -1, "rankmom_252": 1}}


def log(msg: str) -> None:
    print(msg, flush=True)


def load(name: str) -> pd.DataFrame:
    pkl = FACTOR_DIR / f"{name}.pkl.gz"
    pq = FACTOR_DIR / f"{name}.parquet"
    if pq.exists():
        return pd.read_parquet(pq)
    return pd.read_pickle(pkl)


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    log("加载清洗面板、因子、收益率 ...")
    clean = pd.read_pickle(CLEAN_PANEL)[["tradeDate", "ticker", "clean"]]
    frames = [load(n) for n in FACTOR_FILES]
    fac = pd.concat([f.set_index(["tradeDate", "ticker"]) for f in frames], axis=1).reset_index()
    ret = load("returns")  # 含 closePrice
    ret = ret.merge(clean, on=["tradeDate", "ticker"], how="left")
    ret = ret[ret["clean"] == True]  # noqa: E712
    ret = ret.sort_values(["ticker", "tradeDate"]).reset_index(drop=True)
    df = fac.merge(ret[["tradeDate", "ticker"]], on=["tradeDate", "ticker"], how="inner")
    log(f"   清洗后面板: {len(df):,} 行, 用时 {time.time() - t0:.0f}s")

    g_close = ret.groupby("ticker")["closePrice"]
    fwd_ranks = {}
    for h in HORIZONS:
        fwd_h = (g_close.shift(-h) / ret["closePrice"] - 1).astype(np.float32)
        tmp = ret[["tradeDate", "ticker"]].copy()
        tmp[f"fwd_{h}"] = fwd_h
        fwd_ranks[h] = tmp.pivot(index="tradeDate", columns="ticker", values=f"fwd_{h}").rank(axis=1, pct=True)
        log(f"   fwd_{h} 就绪")

    wide_cache: dict[str, pd.DataFrame] = {}

    def get_wide(f: str) -> pd.DataFrame:
        if f not in wide_cache:
            wide_cache[f] = df.pivot(index="tradeDate", columns="ticker", values=f)
        return wide_cache[f]

    targets = FACTORS + ["综合A"]
    rows = []
    for label in targets:
        if label == "综合A":
            parts, counts = None, None
            for f in COMPOSITE_A["factors"]:
                Ff = get_wide(f)
                directed = (Ff.rank(axis=1, pct=True) - 0.5) * COMPOSITE_A["signs"][f]
                parts = directed if parts is None else parts.add(directed, fill_value=0)
                cnt = directed.notna().astype(np.float32)
                counts = cnt if counts is None else counts.add(cnt, fill_value=0)
            F = parts / counts
        else:
            F = get_wide(label)
        f_rank = F.rank(axis=1, pct=True)
        row = {"因子": label}
        for h in HORIZONS:
            ic = f_rank.corrwith(fwd_ranks[h], axis=1).dropna()
            m, s = ic.mean(), ic.std(ddof=1)
            row[f"IC_{h}日"] = round(float(m), 5)
            row[f"ICIR_{h}日"] = round(float(m / s), 3) if s and not np.isnan(s) else np.nan
        rows.append(row)
        log(f"   {label}: " + ", ".join(f"{h}日IC={row[f'IC_{h}日']:.4f}" for h in HORIZONS))

    pd.DataFrame(rows).to_csv(OUT_DIR / "IC衰减.csv", index=False, encoding="utf-8-sig")
    log(f"已保存 IC衰减.csv, 总用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

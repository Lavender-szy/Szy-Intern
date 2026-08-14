# -*- coding: utf-8 -*-
"""
提取市值面板
=====================================================================
从后复权日线 csv 中提取 总市值/流通市值, 用于市值中性化。
输入 : INTERN_CODE/data/raw/stock/MktEqudAdjAfGet/*.csv
输出 : INTERN_CODE/分析结果/factors/market_cap.pkl.gz
       列: tradeDate, ticker, marketValue, negMarketValue
口径 : 与构建因子库一致: 剔除 B 股(200/900 开头), 按 ticker+tradeDate 去重。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

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
DATA_DIR = PROJECT_DIR / "data" / "raw" / "stock" / "MktEqudAdjAfGet"
OUT_DIR = PROJECT_DIR / "分析结果" / "factors"
OUT_PATH = OUT_DIR / "market_cap.pkl.gz"


def main() -> None:
    t0 = time.time()
    files = sorted(DATA_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"目录下没有 csv: {DATA_DIR}")

    frames = []
    for i, f in enumerate(files, 1):
        df = pd.read_csv(
            f,
            usecols=["ticker", "tradeDate", "marketValue", "negMarketValue"],
            dtype={"ticker": "str"},
            encoding="utf-8-sig",
        )
        frames.append(df)
        if i % 1000 == 0 or i == len(files):
            print(f"   已读取 {i}/{len(files)}")

    panel = pd.concat(frames, ignore_index=True)
    panel["tradeDate"] = pd.to_datetime(panel["tradeDate"])
    panel = panel.drop_duplicates(["ticker", "tradeDate"], keep="last")
    panel = panel[~panel["ticker"].str.startswith(("200", "900"))].reset_index(drop=True)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_pickle(OUT_PATH, compression="gzip")
    print(f"市值面板: {len(panel):,} 行, {panel['ticker'].nunique():,} 只股票, "
          f"{panel['tradeDate'].nunique():,} 个交易日")
    print(f"已保存: {OUT_PATH}, 用时 {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
阶段0: 数据口径加固(清洗)
=====================================================================
对应《下一步分析方案.md》阶段0。直接在原始 csv 上打标记:
  is_st        : 名称含 ST / *ST
  is_new       : 上市不足 250 个交易日(以样本内首次出现日近似)
  is_limit     : 触及涨跌停(主板 ±10%, 创业板/科创板 ±20%, ST ±5%;
                 用后复权 closePrice/preClosePrice 近似, 除权日可能有偏差)
  is_suspended : isOpen != 1 或价格缺失
  clean        : 以上全部为 False

输出:
  分析结果/clean/清洗面板.pkl.gz   (含各标记列)
  分析结果/results/清洗统计.csv    (各标记的样本量与占比)
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
DATA_DIR = PROJECT_DIR / "data" / "raw" / "stock" / "MktEqudAdjAfGet"
OUT_DIR = PROJECT_DIR / "分析结果" / "clean"
RESULT_DIR = PROJECT_DIR / "分析结果" / "results"
NEW_MIN_DAYS = 250      # 上市不足 N 个交易日剔除
LIMIT_TOL = 0.003       # 涨跌停判定容差(价格四舍五入误差)


def board_limit(ticker: str, is_st: bool) -> float:
    if is_st:
        return 0.05
    if ticker.startswith(("300", "301", "688", "689")):
        return 0.20
    return 0.10


def main() -> None:
    t0 = time.time()
    files = sorted(DATA_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"目录下没有 csv: {DATA_DIR}")

    print(f"读取 {len(files)} 个 csv ...", flush=True)
    frames = []
    for i, f in enumerate(files, 1):
        df = pd.read_csv(
            f,
            usecols=["ticker", "secShortName", "tradeDate", "preClosePrice",
                     "actPreClosePrice", "closePrice", "isOpen",
                     "marketValue", "negMarketValue"],
            dtype={"ticker": "str", "secShortName": "str", "isOpen": "Int64"},
            encoding="utf-8-sig",
        )
        frames.append(df)
        if i % 1000 == 0 or i == len(files):
            print(f"   已读取 {i}/{len(files)}", flush=True)

    panel = pd.concat(frames, ignore_index=True)
    panel["tradeDate"] = pd.to_datetime(panel["tradeDate"])
    panel = panel.drop_duplicates(["ticker", "tradeDate"], keep="last")
    panel = panel[~panel["ticker"].str.startswith(("200", "900"))].reset_index(drop=True)

    # ---- 标记 ----
    panel["is_st"] = panel["secShortName"].fillna("").str.upper().str.contains("ST")
    # 次新: 样本内第几个交易日
    panel["is_new"] = panel.groupby("ticker").cumcount() < NEW_MIN_DAYS
    # 停牌
    panel["is_suspended"] = (panel["isOpen"] != 1) | panel["closePrice"].isna()
    # 涨跌停
    limit = [board_limit(t, s) for t, s in zip(panel["ticker"], panel["is_st"])]
    panel["limit"] = limit
    ret = panel["closePrice"] / panel["preClosePrice"] - 1
    panel["is_limit_up"] = ret >= panel["limit"] - LIMIT_TOL
    panel["is_limit_down"] = ret <= -panel["limit"] + LIMIT_TOL
    panel["is_limit"] = panel["is_limit_up"] | panel["is_limit_down"]
    panel["clean"] = ~(panel["is_st"] | panel["is_new"] | panel["is_limit"] | panel["is_suspended"])

    # ---- 统计 ----
    n = len(panel)
    stats = {
        "总样本": n,
        "ST": int(panel["is_st"].sum()),
        "次新(<250交易日)": int(panel["is_new"].sum()),
        "涨跌停": int(panel["is_limit"].sum()),
        "停牌/缺失": int(panel["is_suspended"].sum()),
        "清洗后保留": int(panel["clean"].sum()),
    }
    stats_df = pd.DataFrame([{"标记": k, "样本量": v, "占比": f"{v / n:.2%}"}
                             for k, v in stats.items()])
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    stats_df.to_csv(RESULT_DIR / "清洗统计.csv", index=False, encoding="utf-8-sig")
    print(stats_df.to_string(index=False), flush=True)

    # ---- 保存 ----
    out_cols = ["tradeDate", "ticker", "closePrice", "marketValue", "negMarketValue",
                "is_st", "is_new", "is_limit", "is_suspended", "clean"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panel[out_cols].to_pickle(OUT_DIR / "清洗面板.pkl.gz", compression="gzip")
    print(f"已保存: {OUT_DIR / '清洗面板.pkl.gz'}, 用时 {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

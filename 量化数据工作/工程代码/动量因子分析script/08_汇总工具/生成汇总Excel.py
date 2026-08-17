# -*- coding: utf-8 -*-
"""
把全部结果 CSV 汇总到一个 Excel 工作簿, 方便快速翻阅。
输出: 分析结果/最终结果汇总.xlsx
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = Path(r"C:\Users\laven\Desktop\实习\第一周\python学习\INTERN_CODE")
R = PROJECT_DIR / "分析结果" / "results"
OUT = PROJECT_DIR / "分析结果" / "最终结果汇总.xlsx"

SHEETS = [
    ("清洗统计", R / "清洗统计.csv"),
    ("单因子检验(清洗后)", R / "清洗后" / "因子检验汇总.csv"),
    ("相关性_高相关对", R / "高相关因子对.csv"),
    ("市值中性化对比", R / "市值中性化对比.csv"),
    ("月度回测(清洗后)", R / "清洗后" / "月度回测_汇总.csv"),
    ("含成本回测", R / "清洗后" / "含成本回测_汇总.csv"),
    ("市值分层_IC", R / "清洗后" / "市值分层_IC.csv"),
    ("市值分层_多空", R / "清洗后" / "市值分层_月度多空.csv"),
    ("样本外验证", R / "清洗后" / "样本外验证.csv"),
    ("IC衰减", R / "清洗后" / "IC衰减.csv"),
    ("T1成交对比", R / "清洗后" / "T1回测对比.csv"),
    ("综合因子", R / "清洗后" / "综合因子_IC.csv"),
]

with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    for name, path in SHEETS:
        if not path.exists():
            print(f"跳过(不存在): {path.name}")
            continue
        df = pd.read_csv(path, encoding="utf-8-sig")
        df.to_excel(writer, sheet_name=name[:31], index=False)
        print(f"已写入: {name} ({len(df)} 行)")

print(f"完成: {OUT}")

# -*- coding: utf-8 -*-
"""
单因子检验: RankIC / ICIR / 十分位分组收益 / 多空组合
=====================================================================
输入 : 分析结果/factors/ 下由 构建因子库.py 生成的因子文件
输出 : 分析结果/results/
       因子检验汇总.csv   每个因子的 IC/ICIR/多空统计
       分组收益.csv       每个因子按十分位分组的次日收益
       IC序列.csv         每个因子每日的 RankIC 时间序列

检验口径:
  * 预测方向: 用 t 日因子值预测 t+1 日收益 (fwd_ret = ret.shift(-1))
  * RankIC   : 每个交易日, 因子值与次日收益的横截面 Spearman 秩相关
  * ICIR     : IC 均值 / IC 标准差
  * 分组收益 : 每个交易日按因子分 10 组, 组内等权次日收益, 再对时间求平均
  * 多空组合 : 第10组 - 第1组的次日收益

用法:
  python 单因子检验.py                     # 检验全部 4 个因子族
  python 单因子检验.py --family basic_mom  # 只检验某个因子族(可断点续跑)

进度会实时打印; 每个因子完成后写入 done_factors.txt, 中断后重跑会自动跳过.
"""
from __future__ import annotations

import argparse
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
PARTIAL_DIR = RESULT_DIR / "partial"
DONE_FILE = RESULT_DIR / "done_factors.txt"

N_GROUPS = 10
ANNUAL_DAYS = 252
FACTOR_FILES = ["basic_mom", "rank_mom", "smooth_mom", "position"]


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
    """按日期分组的 Spearman 秩相关(向量化, 避免逐日循环)"""
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
    f_rank_all = df.groupby("tradeDate")[factor].rank(pct=True)  # 因子当日横截面分位
    mask = (df[factor].notna() & df["fwd_ret"].notna()).to_numpy()
    date = df["tradeDate"][mask]
    f_rank = f_rank_all[mask]
    r_rank = r_rank_all[mask]
    del f_rank_all

    if len(f_rank) < 1000:
        return None, None, None

    ic = group_ic(f_rank, r_rank, date).dropna()
    n_date = len(ic)
    if n_date < 20:
        return None, None, None

    ic_mean, ic_std = ic.mean(), ic.std(ddof=1)
    icir = ic_mean / ic_std if ic_std and not np.isnan(ic_std) else np.nan
    ic_pos = (ic > 0).mean()
    ic_t = ic_mean / ic_std * np.sqrt(n_date) if ic_std else np.nan

    # 分位数值在大量并列时会导致整组被吞掉(如 position 因子), 因此按横截面名次分十组,
    # 保证每天 10 组都有股票且组间均衡; IC 仍用平均秩(pct rank)计算, 不受影响.
    f_rank_ord_all = df.groupby("tradeDate")[factor].rank(method="first")  # 1..N
    n_daily_all = df.groupby("tradeDate")[factor].transform("count")       # 当日有效数 N
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
        "因子名": factor,
        "因子族": fam,
        "窗口": window,
        "IC均值": round(float(ic_mean), 5),
        "IC标准差": round(float(ic_std), 5),
        "ICIR": round(float(icir), 4),
        "IC>0占比": round(float(ic_pos), 4),
        "IC_t": round(float(ic_t), 3),
        "多空日收益": round(float(ls_mean), 6),
        "多空年化": round(float(ls_mean * ANNUAL_DAYS), 4),
        "多空_t": round(float(ls_t), 3),
        "检验天数": int(n_date),
    }
    group_data = pd.DataFrame({
        "因子名": factor,
        "组别": range(1, N_GROUPS + 1),
        "组均日收益": [round(v, 6) for v in gmean.fillna(0).tolist()],
        "年化": [round(v * ANNUAL_DAYS, 4) for v in gmean.fillna(0).tolist()],
        "组_t": [round(v, 3) for v in gt.fillna(0).tolist()],
    })
    return row, group_data, ic


def save_partials(factor: str, row: dict, gdf: pd.DataFrame, ic: pd.Series) -> None:
    summary_path = RESULT_DIR / "因子检验汇总.csv"
    pd.DataFrame([row]).to_csv(summary_path, mode="a",
                               header=not summary_path.exists(),
                               index=False, encoding="utf-8")
    gdf.to_csv(PARTIAL_DIR / f"groups_{factor}.csv", index=False, encoding="utf-8")
    ic_df = pd.DataFrame({
        "日期": [d.strftime("%Y-%m-%d") for d in ic.index],
        "因子名": factor,
        "IC": ic.round(5).to_numpy(),
    })
    ic_df.to_csv(PARTIAL_DIR / f"ic_{factor}.csv", index=False, encoding="utf-8")


def finalize() -> None:
    summary_path = RESULT_DIR / "因子检验汇总.csv"
    if summary_path.exists():
        pd.read_csv(summary_path, encoding="utf-8") \
            .sort_values("ICIR", ascending=False, na_position="last") \
            .to_csv(summary_path, index=False, encoding="utf-8-sig")

    gfiles = sorted(PARTIAL_DIR.glob("groups_*.csv"))
    if gfiles:
        pd.concat([pd.read_csv(f, encoding="utf-8") for f in gfiles], ignore_index=True) \
            .to_csv(RESULT_DIR / "分组收益.csv", index=False, encoding="utf-8-sig")

    ifiles = sorted(PARTIAL_DIR.glob("ic_*.csv"))
    if ifiles:
        pd.concat([pd.read_csv(f, encoding="utf-8") for f in ifiles], ignore_index=True) \
            .to_csv(RESULT_DIR / "IC序列.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=FACTOR_FILES, default=None,
                        help="只检验某个因子族(默认全部)")
    args = parser.parse_args()

    t0 = time.time()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    PARTIAL_DIR.mkdir(parents=True, exist_ok=True)

    done = set()
    if DONE_FILE.exists():
        done = set(DONE_FILE.read_text(encoding="utf-8").splitlines())
    if done:
        log(f"检测到 {len(done)} 个已完成因子, 将自动跳过")

    targets = [args.family] if args.family else FACTOR_FILES

    log("加载 returns ...")
    ret = load("returns")
    ret["fwd_ret"] = ret.groupby("ticker")["ret"].shift(-1)
    ret = ret[["tradeDate", "ticker", "ret", "fwd_ret"]].astype({c: np.float32 for c in ("ret", "fwd_ret")})

    for fam in targets:
        log(f"加载 {fam} ...")
        fac = load(fam)
        t1 = time.time()
        df = fac.merge(ret, on=["tradeDate", "ticker"], how="left")
        log(f"   merge 完成, 用时 {time.time() - t1:.0f}s, 共 {len(df):,} 行")
        r_rank_all = df.groupby("tradeDate")["fwd_ret"].rank(pct=True)

        for factor in [c for c in fac.columns if c not in ("tradeDate", "ticker")]:
            if factor in done:
                log(f"跳过 {factor} (已完成)")
                continue
            t2 = time.time()
            row, gdf, ic = test_one(df, factor, r_rank_all)
            if row is None:
                log(f"{factor}: 有效样本不足, 跳过")
                continue
            save_partials(factor, row, gdf, ic)
            with DONE_FILE.open("a", encoding="utf-8") as f:
                f.write(factor + "\n")
            log(f"{factor}: IC={row['IC均值']}, ICIR={row['ICIR']}, "
                f"多空日收益={row['多空日收益']}, 多空_t={row['多空_t']}, "
                f"用时 {time.time() - t2:.0f}s")
        del df, fac

    finalize()
    summary_path = RESULT_DIR / "因子检验汇总.csv"
    if summary_path.exists():
        summary = pd.read_csv(summary_path, encoding="utf-8-sig")
        log("\n按 ICIR 排序的检验结果(前 15):")
        log(summary.head(15).to_string(index=False))
    log(f"\n完成, 总用时 {time.time() - t0:.0f} 秒, 结果目录: {RESULT_DIR}")


if __name__ == "__main__":
    main()

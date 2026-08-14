#1.导入
from datetime import date
from pathlib import Path
import time
import pandas as pd

from client import DataAPI


#2.配置常量
PROJECT_DIR = Path(__file__).resolve().parent
BEGIN_DATE = "20150101"
END_DATE = date.today().strftime("%Y%m%d")
OUTPUT_DIR = PROJECT_DIR / "data" / "raw" / "stock" / "MktEqudAdjAfGet"
BATCH_SIZE = 1500
BATCH_NO = 4  # 从 0 开始，n 表示第 n+1 批


#3.函数定义
#3.1接口数据dataframe函数，获取股票基本资料
def get_stock_info():
    stock_info = DataAPI.SecIDGet(
        partyID="",
        ticker="",
        cnSpell="",
        assetClass="E", #股票类资产
        secShortName="",
        exchangeCD="XSHE,XSHG", #深交所 ，上交所
        listStatusCD="L", #当前上市
        field="ticker,secShortName,exchangeCD,listDate,listStatusCD",
        pandas="1",
    )
    return stock_info


#3.2提取ticker列函数
def get_tickers(stock_info):
    tickers = stock_info["ticker"].dropna().astype(str).tolist()
    return tickers


#3.3选择本次下载批次函数
def select_batch(tickers, batch_no, batch_size):
    start = batch_no * batch_size
    end = min(start + batch_size, len(tickers))
    return tickers[start:end], start, end


#3.4获取单只股票数据函数
def get_stock_data(ticker, begin_date, end_date):
    data = DataAPI.MktEqudAdjAfGet(
        secID="",
        ticker=ticker,
        tradeDate="",
        beginDate=begin_date,
        endDate=end_date,
        isOpen="",
        field="",
        pandas="1",
    )
    return data

#3.5读取最后一个交易日函数
def get_last_trade_date(output_dir, ticker):
    output_path = output_dir / f"{ticker}.csv"
    data = pd.read_csv(output_path, dtype={"tradeDate": str})
    return data["tradeDate"].max()

#3.6下载并保存一支股票函数
def download_one_stock(ticker, output_dir, begin_date, end_date):
    output_path = output_dir / f"{ticker}.csv"
    old_data = None
    if output_path.exists():
        begin_date = get_last_trade_date(output_dir, ticker)
        old_data = pd.read_csv(output_path, dtype={"tradeDate": str})
    try:
        data = get_stock_data(ticker, begin_date, end_date)
    except Exception as error:
        print(f"{ticker}下载失败：{error}")
        return "failed"
    if data.empty:
        print(f"{ticker}没有查询到数据")
        return "empty"
    data["tradeDate"] = data["tradeDate"].astype(str)
    if old_data is not None:
        data = pd.concat([old_data, data])
        data = data.drop_duplicates(subset=["tradeDate"], keep="last")
    data = data.sort_values(by="tradeDate").reset_index(drop=True)
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"{ticker}下载完成，共{len(data)}行，保存到：{output_path}")
    return "success"


#-------------------------------------------
#4.执行流程
def main():
    result_count = {
    "success": 0,
    "empty": 0,
    "failed": 0,
    }

    #4.1获取股票基本资料
    stock_info = get_stock_info()

    print(stock_info.head())
    print(f"股票数量：{len(stock_info)}")

    #4.2提取ticker列
    tickers = get_tickers(stock_info)

    #4.3选择本次下载批次
    download_tickers, start, end = select_batch(tickers, BATCH_NO, BATCH_SIZE)
    if not download_tickers:
        print("本批次没有股票，请检查BATCH_NO")
        return

    print(f"本次下载第 {BATCH_NO + 1} 批")
    print(f"股票范围：{start} 到 {end-1}")
    print(f"本次股票数量：{len(download_tickers)}")

    #4.4按股票循环抓取数据
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for number, ticker in enumerate(download_tickers, start=1):
        print(f"正在下载第 {number} 只股票：{ticker}")
        result = download_one_stock(ticker, OUTPUT_DIR, BEGIN_DATE, END_DATE)
        result_count[result] += 1
        time.sleep(0.5) #跳过时没有访问数据接口，不需要休眠

    print(f"成功数量：{result_count['success']}")
    print(f"空数据数量：{result_count['empty']}")
    print(f"失败数量：{result_count['failed']}")

if __name__ == "__main__":
    main()
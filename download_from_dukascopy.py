from lzma import LZMADecompressor, LZMAError, FORMAT_AUTO
import optparse
import os, copy
import struct
from datetime import datetime, timedelta
from urllib import request
from urllib.error import HTTPError
from core.mongodb import Mongodb
import calendar
import pandas as pd

pymongo = Mongodb(host='127.0.0.1', port=27017)

def get_weekday(datetime_obj, week_day="monday"):
    """
    获取指定时间的当周的星期x
    :param datetime_obj: 时间
    :param week_day: 指定的星期x
    :return:
    """
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),
                 range(7)))  # datetime 模块中，星期一到星期天对应数字 0 到 6
    delta_hour = timedelta(days=1)  # 改变幅度为 1 天
    while datetime_obj.weekday() != d.get(week_day):
        if datetime_obj.weekday() > d.get(week_day):
            datetime_obj -= delta_hour
        elif datetime_obj.weekday() < d.get(week_day):
            datetime_obj += delta_hour
        else:
            pass
    return datetime_obj


def get_first_weekday(year, month, n=1, w="monday"):
    """
    获取 year 年，month 月 的第n个星期w和倒数第n个星期w的日期
    :param year: 指定年份，如 2019
    :param month: 指定月份，如 6
    :param n: 第n个
    :param w: 指定的星期w
    :return:
    """
    # 获取第一和最后一天
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),
                 range(7)))  # datetime 模块中，星期一到星期天对应数字 0 到 6
    weekday, count_day = calendar.monthrange(year=year,
                                             month=month)  # 返回指定月份第一天（即1号）的星期日期，和本月的总天数 https://blog.csdn.net/tz_zs/article/details/86629959
    first_day = datetime(year=year, month=month, day=1)  # <type 'datetime.datetime'>
    last_day = datetime(year=year, month=month, day=count_day)
    # first_day, last_day = get_month_firstday_and_lastday(year=year, month=month, n=1)

    # 第1个星期w
    if first_day.weekday() > d.get(w):  # 说明本周的星期w在上个月
        datetime_obj = first_day + timedelta(weeks=1)
    else:
        datetime_obj = first_day
    datetime_obj += timedelta(weeks=n - 1)
    first_weekday = get_weekday(datetime_obj=datetime_obj, week_day=w)

    return first_weekday


def decompress_lzma(data):
    results = []
    len(data)
    while True:
        decomp = LZMADecompressor(FORMAT_AUTO, None, None)
        try:
            res = decomp.decompress(data)
        except LZMAError:
            if results:
                break
            else:
                raise
        results.append(res)
        data = decomp.unused_data
        if not data:
            break
        if not decomp.eof:
            raise LZMAError("Compressed data ended before the end-of-stream marker was reached")
    return b"".join(results)


def tokenize(buffer):
    token_size = 20
    token_count = int(len(buffer) / token_size)
    tokens = list(map(lambda x: struct.unpack_from('>3I2f', buffer, token_size * x), range(0, token_count)))
    return tokens


def normalize_tick(symbol, day, time, ask, bid, ask_vol, bid_vol):
    date = day + timedelta(milliseconds=time)

    # TODO 網羅する。この通過ペア以外も有るかも
    if any(map(lambda x: x in symbol.lower(), ['usdrub', 'xagusd', 'xauusd', 'jpy'])):
        point = 1000
    else:
        point = 100000

    return [date, ask / point, bid / point, round(ask_vol * 1000000), round(bid_vol * 1000000)]


def format_to_csv_for_ticks(ticks):
    df = pd.DataFrame(ticks, columns=['date', 'Ask', 'Bid', 'AskVolume', 'BidVolume'])
    df = df.drop(['Ask', 'AskVolume', 'BidVolume'], axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def format_to_csv_for_candle(ticks, scale,price_type):
    df = pd.DataFrame(ticks, columns=['date', 'Ask', 'Bid', 'AskVolume', 'BidVolume'])
    if price_type=="bid":
        df = df.drop(['Ask', 'AskVolume', 'BidVolume'], axis=1)
    else:
        df = df.drop(['Bid', 'AskVolume', 'BidVolume'], axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    if scale.lower() in ["4h","1d"]:
        # is_dst_result = is_dst(df.index[0])
        is_dst_result, _, _ = is_dst(datetime.strptime(df.index[0].strftime("%Y-%m-%d"), "%Y-%m-%d"))
        if is_dst_result:
            # 夏令时，4h的开始时间是凌晨1点
            h4_start_hour = "21h"
        else:
            h4_start_hour = "22h"
        df_ohlc = df.resample(scale, offset=h4_start_hour).ohlc()
        df_ohlcv = df_ohlc.assign(Volume=df.iloc[:, 0].resample(scale, offset=h4_start_hour).count())
    else:
        df_ohlc = df.resample(scale).ohlc()
        df_ohlcv = df_ohlc.assign(Volume=df.iloc[:, 0].resample(scale).count())

    return df_ohlcv


def is_dst(day):
    dst_start = get_first_weekday(year=day.year, month=3, n=2, w="sunday")
    dst_end = get_first_weekday(year=day.year, month=11, n=1, w="sunday")
    if dst_start <= day < dst_end:
        return True, dst_start, dst_end
    return False, dst_start, dst_end


def load_bi5(path, symbol, day: datetime):
    file_name = f'{day.hour:02d}h_ticks.bi5'
    file_path = f'{path}\{symbol}\{day.year:04d}\{day.month - 1:02d}\{day.day:02d}\{file_name}'
    print(f'loading: {file_path}')

    # req = request.Request(url)
    try:
        with open(file_path, "rb") as res:
            res_body = res.read()
    except Exception as e:
        print('load failed. continuing...save_path=%s' % file_path)

        url_prefix = 'https://datafeed.dukascopy.com/datafeed'
        url = f'{url_prefix}/{symbol}/{day.year:04d}/{day.month - 1:02d}/{day.day:02d}/{file_name}'
        print("download url:%s" % url)
        if not os.path.exists(file_path[:file_path.rfind("\\")]):
            os.makedirs(file_path[:file_path.rfind("\\")])
        req = request.Request(url)
        try:
            with request.urlopen(req) as res:
                if res.code == 200:
                    res_body = res.read()

                    with open(file_path, "wb") as f:
                        f.write(res_body)
                else:
                    print("download fail:%s" % url)
        except HTTPError:
            print('download failed. continuing..')

    data = []
    if len(res_body):
        try:
            data = decompress_lzma(res_body)
        except LZMAError:
            print('decompress failed. continuing..')

    tokenized_data = tokenize(data)

    ticks_hour = list(map(lambda x: normalize_tick(symbol, day, *x), tokenized_data))
    return ticks_hour


def from_local_path(path, symbol, day):
    ticks_day = []

    result, dst_start, dst_end = is_dst(day)
    if result:
        end_time = day + timedelta(hours=0) + timedelta(days=1)
        if dst_start == day:
            day += timedelta(hours=20)

        while True:
            if day == end_time:
                break
            day = day + timedelta(hours=1)
            ticks_hour = load_bi5(path, symbol, day)
            ticks_day.extend(ticks_hour)
    else:
        if dst_start == day + timedelta(days=1):
            return []
        end_time = day + timedelta(hours=22) + timedelta(days=1)
        if dst_end == day:
            day = day + timedelta(hours=-2)
        else:
            day = day + timedelta(hours=-2) + timedelta(days=1)
        while True:
            if day == end_time:
                break

            ticks_hour = load_bi5(path, symbol, day)
            day = day + timedelta(hours=1)
            ticks_day.extend(ticks_hour)
    print("end...........")
    return ticks_day


def main():
    parser = optparse.OptionParser(
        usage='Usage: python {} [options] <symbol> <start: yyyy-mm-dd> <end: yyyy-mm-dd>'.format(
            os.path.basename(__file__)))
    parser.add_option('-c', action="store", metavar='time_scale', dest="c", help="candlestick. ex: 1min, 1H, 1D")
    parser.add_option('-d', action="store", metavar='output_dir', dest="d", default='./', help="output directory.")
    parser.add_option('-t', action="store", metavar='price_type', dest="t", default='bid', help="select price type")
    parser.add_option('--mongo', action="store_true", help="save data to mongodb")
    parser.add_option('-s', action="store", metavar='source_dir', dest="s", default='./', help="source data directory.")

    (options, args) = parser.parse_args()

    if len(args) < 3:
        parser.print_help()
        exit(1)

    symbol = args[0].upper()
    start_date = datetime.strptime(args[1], '%Y-%m-%d')
    end_date = datetime.strptime(args[2], '%Y-%m-%d')

    save_mongo = True if options.mongo else False
    output_dir = options.d
    output_suffix = f'_{options.c}' if options.c is not None else ''
    output_csv = f'{output_dir}/{symbol}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}{output_suffix}_{options.t}.csv'

    d = start_date

    result_df = pd.DataFrame()
    while d <= end_date:
        df=pd.DataFrame()
        ticks_day = from_local_path(options.s, symbol, d)


        if options.c is None:

            df = format_to_csv_for_ticks(ticks_day)
            result_df = pd.concat([result_df, df])
            # result_df.columns = ["bid"]

        else:
            if ticks_day:
                df = format_to_csv_for_candle(ticks_day, options.c, options.t)
                df.columns = ["open", "high", "low", "close", "volume"]



                result_df = pd.concat([result_df, df])

            # f.write(format_to_csv_for_candle(ticks_day, options.c))

        d += timedelta(days=1)

        if save_mongo:
            try:
                df = df.reset_index()
                df["complete"]=1.0
                df["date"]=df["date"].astype(str)
                df["volume"] = df['volume'].astype(float)
                df['timestamp'] = df["date"].apply(lambda x: x.split(" ")[1])
                data=df.to_dict(orient='records')
                pymongo.conn["EUR_USD_duka" ]["M1"].insert_many(data)
            except Exception as e:
                print(e)

    if not save_mongo:
        result_df.to_csv(output_csv)


if __name__ == '__main__':
    main()

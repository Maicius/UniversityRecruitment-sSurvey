# coding=utf-8
import time

# 工具类
import traceback


def get_header(host):
    header = {
        'host': host,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'
    }
    return header


def get_short_date(date):
    time_array = time.strptime(date, "%Y-%m-%d")
    return time.strftime("%Y%m%d", time_array)


# %a 星期的简写。如 星期三为Web
# %A 星期的全写。如 星期三为Wednesday
# %b 月份的简写。如4月份为Apr
# %B 月份的全写。如4月份为April
# %c:  日期时间的字符串表示。（如： 04/07/10 10:43:39）
# %d:  日在这个月中的天数（是这个月的第几天）
# %f:  微秒（范围[0,999999]）
# %H:  小时（24小时制，[0, 23]）
# %I:  小时（12小时制，[0, 11]）
# %j:  日在年中的天数 [001,366]（是当年的第几天）
# %m:  月份（[01,12]）
# %M:  分钟（[00,59]）
# %p:  AM或者PM
# %S:  秒（范围为[00,61]，为什么不是[00, 59]，参考python手册~_~）
# %U:  周在当年的周数当年的第几周），星期天作为周的第一天
# %w:  今天在这周的天数，范围为[0, 6]，6表示星期天
# %W:  周在当年的周数（是当年的第几周），星期一作为周的第一天
# %x:  日期字符串（如：04/07/10）
# %X:  时间字符串（如：10:43:39）
# %y:  2个数字表示的年份
# %Y:  4个数字表示的年份
# %z:  与utc时间的间隔 （如果是本地时间，返回空字符串）
# %Z:  时区名称（如果是本地时间，返回空字符串）
# %%:  %% => %
# Oct 19, 2017 12:00:00 AM
# May 27, 2015 12:00:00 AM

def get_standard_date(date):
    time_array = time.strptime(date, "%b %d, %Y %X %p")
    return time.strftime("%Y-%m-%d", time_array)


def get_standard_date2(date):
    time_array = time.strptime(date, "%Y-%m-%d %X")
    return time.strftime("%Y-%m-%d", time_array)


# 将字符串时间转换为时间戳
def get_mktime(date_string):
    return time.mktime(time.strptime(date_string, '%Y-%m-%d'))


def get_month(date):
    time_array = time.strptime(str(date), "%Y-%m-%d")
    return time.strftime("%Y-%m", time_array)


def format_err(e, item1='', item2=''):
    print("error*************************************************************")
    print(e)
    print(item1)
    print(item2)
    print("error*************************************************************")

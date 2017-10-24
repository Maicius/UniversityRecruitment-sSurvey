import redis
import time


class jedis(object):

    def __init__(self):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
        self.re = redis.Redis(connection_pool=pool)

    def connect_redis(self):
        return self.re

    def save_info(self, name,  date, company_name):
        self.re.lpush(name, {"date": date, "company_name": company_name})

    def save_infos(self, name,  item):
        self.re.lpush(name, item)

    def save_company_info(self, name, company_rank, company_name,company_industry,company_contry,  company_profit,
                          company_people_num, company_type):
        self.re.lpush(name, {"company_rank": company_rank, "company_name": company_name,"company_contry": company_contry,
                             "company_industry": company_industry,"company_profit": company_profit,
                             "company_people_num": company_people_num, "company_type": company_type})

    # 维持一个大学列表，记录每个大学list的名称
    def add_university(self, name):
        self.re.lpush("university", name)


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


def get_standard_date(date):
    time_array = time.strptime(date, "%b %d, %Y %X %p")
    return time.strftime("%Y-%m-%d", time_array)


def get_standard_date2(date):
    time_array = time.strptime(date, "%Y-%m-%d %X")
    return time.strftime("%Y-%m-%d", time_array)


def get_month(date):
    time_array = time.strptime(str(date), "%Y-%m-%d")
    return time.strftime("%Y-%m", time_array)

if __name__ == '__main__':
    # re = jedis()
    # re.connect_redis()
    # re.add_university("scu_company_info")
    # re.add_university("thu_company_info")
    # re.add_university("nju_company_info")
    # re.add_university("sjtu_company_info")
    # re.add_university("jincheng_company_info")
    # re.add_university("lzu_company_info")
    str1 = "Oct 19, 2017 12:00:00 AM"
    # str1 = str1[0:12]
    time = get_standard_date(str1)
    print(time)
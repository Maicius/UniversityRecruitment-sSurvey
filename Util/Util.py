import json
import traceback

import redis
import time

# 封装redis的操作，统一数据接口
# 为没有安装redis的用户提供保存到json文件的接口
class jedis(object):
    def __init__(self):
        # 使用redis保存数据，如果没有redis须注释掉这两句代码

        # 使用json文件保存数据
        self.data_array = []
        self.host = "127.0.0.1"
        self.port = "6379"
        self.re = self.get_re()

    # 返回一个原生的redis对象
    def get_re(self):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)
        re = redis.StrictRedis(connection_pool= pool)
        return re

    def connect_redis(self):
        return self.re

    # 保存数据，将传入的date 和company_name 格式化为字典再保存
    def save_info(self, name, date, company_name):
        data = {"date": date, "company_name": company_name}
        self.save_dict(name, data)

    # 保存字典格式的数据
    def save_dict(self, name, data):
        # 如果不使用redis也要注释掉这句
        self.re.lpush(name, data)

        # 将数据缓存到data_array中，最终保存数据
        self.data_array.append(data)

    def save_infos(self, name, item):
        self.re.lpush(name, item)

    def save_company_info(self, name, company_rank, company_name, company_industry, company_contry, company_profit,
                          company_people_num, company_type):
        self.re.lpush(name,
                      {"company_rank": company_rank, "company_name": company_name, "company_contry": company_contry,
                       "company_industry": company_industry, "company_profit": company_profit,
                       "company_people_num": company_people_num, "company_type": company_type})

    # 维持一个大学列表，记录每个大学list的名称
    def add_university(self, name):
        self.re.lpush("university", name)

    def add_to_file(self, name):
        with open('../data/' + name + '.json', 'w+', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)

    def test_add_to_file(self):
        self.add_to_file("test")

    def handle_error(self, e, name):
        msg = traceback.format_exc(e)
        print(msg)
        print("Unexpected Error")
        print("The program will save the data and exit")
        # 程序意外退出时保存文件
        self.add_to_file(name)

    def print_redis_error(self, e):
        msg = traceback.format_exc(e)
        print(msg)
        print("redis failed to connect, please check redis config")
        print("now the data would to save into json file only")


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
    re = jedis()
    re.connect_redis()
    re.add_university("scu_company_info")
    re.add_university("thu_company_info")
    re.add_university("nju_company_info")
    re.add_university("sjtu_company_info")
    re.add_university("jincheng_company_info")
    re.add_university("lzu_company_info")
    re.add_university("ustc_company_info")
    re.add_university("cufe_company_info")
    # str1 = "Oct 19, 2017 12:00:00 AM"
    # # str1 = str1[0:12]
    # time = get_standard_date(str1)
    # print(time)
    # re = jedis()
    # re.test_add_to_file()

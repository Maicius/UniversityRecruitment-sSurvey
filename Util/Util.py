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

    def save_infos(self,name,  item):
        self.re.lpush(name, item)

    def save_company_info(self, name, company_rank, company_name,company_industry,company_contry,  company_profit, company_people_num, company_type):
        self.re.lpush(name, {"company_rank": company_rank, "company_name": company_name,"company_contry":company_contry, "company_industry": company_industry,
                             "company_profit": company_profit, "company_people_num": company_people_num, "company_type": company_type})

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
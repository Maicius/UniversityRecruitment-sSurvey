import redis
import time


def connect_redis():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
    re = redis.Redis(connection_pool=pool)
    print("connect to redis successful")
    return re

def get_header(host):
    header = {
        'host': host,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'cookie': 'JSESSIONID=abcHgElBfU2Gy4caRAd9v; thuwebcookie=1795452682.20480.0000'
    }
    return header

def get_short_date(date):
    time_array = time.strptime(date, "%Y-%m-%d")
    return time.strftime("%Y%m%d", time_array)
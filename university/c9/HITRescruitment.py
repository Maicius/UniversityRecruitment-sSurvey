# coding = utf-8
import datetime
import json
import requests
from jedis import jedis
from util import util

# 哈尔滨工业大学
table_name = "hit_company_info_2018"


def get_hit_rescruit():
    print("HIT Begin ===================================================")
    base_url = "http://job.hit.edu.cn/index/getZczphData"
    host = "job.hit.edu.cn"
    header = util.get_header(host)

    req = requests.Session()
    header[
        'Cookie'] = 'UM_distinctid=12d92-04155388a776ed-49566e-1fa400-15fef2bf12e643; CNZZDATA1261107882=1341678225-1511543504-https%253A%252F%252Fwww.baidu.com%252F%7C1513672466; JSESSIONID=E8EAAFC1F662C83D57C2D504594BD6CF'
    # res = req.get("http://job.hit.edu.cn/info?dj=MQ--").content.decode('utf-8')
    # print(res)
    # req.headers.update()
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    # 哈工大最新的就业网站是从2016年9月开始的
    for i in range(0, 16):
        month = 9
        year = 2016
        month = month + i
        if month > 12:
            year = 2017
            month = month - 12

        date = datetime.date(year, month, 1)
        params = {'Month': util.get_month(date)}
        # params = {'Month': '2017-11'}
        params = json.dumps(params)
        print(params)
        print(base_url)
        res = req.post(url=base_url, headers=header, data=params)
        print(res.status_code)
        content = res.content.decode("utf-8")
        # print(content)
        parse_hit_info(content, re)
    re.add_to_file(table_name)
    re.add_university(table_name)
    print("HIT finish ===================================================")


def parse_hit_info(content, re):
    content = json.loads(content)
    for item in content['module']:
        company_name = item['ZCZPHMC']
        date = item['ZPHRQ']
        date = util.get_standard_date2(date)
        print(company_name)
        print(date)
        re.save_info(table_name, date, company_name)


if __name__ == '__main__':
    get_hit_rescruit()

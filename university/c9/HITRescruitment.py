# coding = utf-8
import datetime
import json
import requests
from jedis import jedis
from util import util


# 哈尔滨工业大学
table_name = "hit_company_info"
def get_hit_rescruit():
    print("HIT Begin ===================================================")
    base_url = "http://job.hit.edu.cn/index/getZczphData"
    host = "job.hit.edu.cn"
    header = util.get_header(host)
    header['referer'] = "http://job.hit.edu.cn/info?dj=MQ--"
    header['accept'] = "*/*"
    header['X-Requested-With'] = "XMLHttpRequest"
    req = requests.Session()
    header['cookie'] = "JSESSIONID=A36AAA74D82B3F39C3FD2455853EC081"
    req.get("http://job.hit.edu.cn/info?dj=MQ--")
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    # 哈工大最新的就业网站是从2016年9月开始的，至今一共有13个月的数据
    for i in range(0, 16):
        month = 9
        year = 2016
        month = month + i
        if month > 12:
            year = 2017
            month = month - 12

        date = datetime.date(year, month, 1)
        params = {'Month': util.get_month(date)}
        # params = {'Month': '2017-10'}
        params = json.dumps(params)
        print(params)
        res = req.post(headers=header, url=base_url, data=params)
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

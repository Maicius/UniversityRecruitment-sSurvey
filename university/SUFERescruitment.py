# coding=utf-8
import json

import requests

from jedis import jedis
from util import util


def get_sufe_recruit():
    host = "career.sufe.edu.cn/"
    headers = util.get_header(host)
    re = jedis.jedis()
    re.connect_redis()

    url = "http://careersys.sufe.edu.cn/pros_jiuye/s/zxh/owebsiteData/recruitmentAndPreaching?callback=&type=list&eachPageRows=413&currentPageno=1&_="
    req = requests.Session()
    res = req.get(headers=headers, url=url)
    content = res.content.decode("utf-8")
    parse_info(content, re)


def parse_info(content, re):
    print(content)
    length = len(content)
    info = content[1: length - 1]
    company_dict = json.loads(info)
    i = 0
    for item in company_dict['listData']:
        print(i)
        company_name = item['yrdwname']
        date = item['apjssj'][:10]
        i +=1
        re.save_info("sufe_company_info", date, company_name)



if __name__ == '__main__':
    get_sufe_recruit()
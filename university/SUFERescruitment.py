# coding=utf-8
import requests

from util import util


def get_sufe_recruit():
    host = "career.sufe.edu.cn/"
    headers = util.get_header(host)
    url = "http://careersys.sufe.edu.cn/pros_jiuye/s/zxh/owebsiteData/recruitmentAndPreaching?callback=&type=list&eachPageRows=500&currentPageno=1&_="
    req = requests.Session()
    res = req.get(headers=headers, url=url)
    content = res.content.decode("utf-8")
    parse_info(content)


def parse_info(content):
    print(content)



if __name__ == '__main__':
    get_sufe_recruit()
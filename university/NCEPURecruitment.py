import requests
from bs4 import BeautifulSoup
import re
from Util import Util


# 华北电力大学
# 包括宣讲会与双选会
def get_ncepu_recruit():
    table_name = "ncepu_table_name"
    base_url = "http://job.ncepu.edu.cn/teachin/index?domain=ncepu&page="
    req = requests.Session()
    redis = Util.jedis()
    redis.connect_redis()
    host = "job.ncepu.edu.cn"
    header = Util.get_header(host)
    # 获取宣讲会信息
    for i in range(1, 2):
        res = req.get(headers=header, url=base_url + str(i))
        html = res.content.decode("utf-8")
        # parse_info(html, redis, table_name)
    get_double_choose(req, header, re)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def get_double_choose(req, header, redis):
    url = "http://job.ncepu.edu.cn/jobfair/index?domain=ncepu"
    content = req.get(url= url, headers=header).content
    html = content.decode("utf-8")
    soup = BeautifulSoup(html, "html5lib")
    com_list = soup.find_all(href=re.compile('/jobfair/view/id'))
    for item in com_list:
        detail_url = item.get('href')
        print(detail_url)
        detail_url = "http://job.ncepu.edu.cn" + detail_url
        detail = req.get(url=detail_url, headers=header).content.decode("utf-8")
        detail_soup = BeautifulSoup(detail, "html5lib")
        detail_text = detail_soup.text
        # 由于格式十分不固定，所以使用正则表达式来提取内容
        companys = detail_text.find("详情")
        print(companys)

    print(com_list)

def parse_info(html, re, table_name):
    soup = BeautifulSoup(html, "html5lib")
    company_list = soup.find_all("")
    print(company_list)
    try:
        for j in range(3, 24):
            infos = company_list[j].text.split("\n")
            company_name = infos[1].strip()
            date = infos[5].strip()[0:10]
            print(company_name)
            print(date)
            re.save_info(table_name, date, company_name)
    except IndexError:
        print("finish")
    except ConnectionError as e:
        re.handle_error(e, table_name)


if __name__ == '__main__':
    get_ncepu_recruit()
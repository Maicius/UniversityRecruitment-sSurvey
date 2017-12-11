# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

from jedis import jedis
from util import util

table_name = 'szu_company_info'
# 深圳大学
def get_szu_recruit():
    print("深圳大学开始==================================")
    url = 'http://job.szu.edu.cn/EngageListAllMeeting.aspx?index=1'
    headers = util.get_header('job.szu.edu.cn')
    req = requests.session()
    redis = jedis.jedis()
    redis.clear_list(table_name)
    content = req.get(url=url, headers=headers).content.decode("utf-8")
    base_url = url[0:-1]
    total_num = get_total_page(content)
    for i in range(1, total_num + 1):
        url = base_url + str(i)
        print(url)
        content = req.get(url=url, headers=headers).content.decode("utf-8")
        parse_info(content, redis)
    redis.add_university(table_name)
    redis.add_to_file(table_name)
    print("深圳大学结束==================================")


def parse_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    company_list = soup.find_all(href=re.compile('engage-'))
    date_list = re.findall(re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}'), str(soup))
    for i in range(len(company_list)):
        company_name = company_list[i].text.strip()
        date = date_list[i].strip()
        print(company_name, date)
        redis.save_info(table_name, date, company_name)


def get_total_page(content):
    soup = BeautifulSoup(content, 'html5lib')
    total_page = re.findall(re.compile('/[0-9]{2}页'), str(soup))
    print(total_page)
    return int(total_page[0][1:-1])


if __name__ == '__main__':
    get_szu_recruit()

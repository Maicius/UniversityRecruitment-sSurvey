# coding = utf-8
import re
import requests
from bs4 import BeautifulSoup

from jedis import jedis
from util import util

# 云南大学
table_name = 'ynu_company_info'
headers = util.get_header('jobs.ynu.edu.cn')
req = requests.Session()
date_pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')


def get_ynu_recruitment():
    base_url = "http://jobs.ynu.edu.cn/wszplist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1091"
    url = 'http://jobs.ynu.edu.cn/wszplist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1091'

    redis = jedis.jedis()
    redis.clear_list(table_name)
    content = req.get(url=base_url, headers=headers).content.decode('utf-8')
    total_page_num = get_total_num(content)
    params = {
        'reqformCURURI': '3187540095DC12E6C9C66ED4973512AD',
        'reqformKEYTYPES': '4, 12, 93',
        'actiontype': 'Find',
        'reqformORDER': 'desc',
        'reqformORDERKEY': 'wbrelease',
        'reqformCountNo': total_page_num,
        'reqformGOPAGE': '',
        'reqformINTEXT': '',
        'reqformNOWPAGE': '',
        'reqformPAGE': 0,
        'reqformrowCount': total_page_num
    }
    # 一次性获取所有招聘会信息
    content = req.post(url=base_url, headers=headers, data=params).content.decode('utf-8')
    parse_info(content, redis)
    # 获取选双选会数据
    url = 'http://jobs.ynu.edu.cn/dxzplist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1093'
    params = {
        'reqformCURURI': 'BFE8E8F659EBC3C487ADA586A2CC75B6',
        'reqformKEYTYPES': '4, 12, 93, 4, 12',
        'actiontype': 'Find',
        'reqformORDER': 'desc',
        'reqformORDERKEY': 'wbrecruitdate',
        'reqformCountNo': 50,
        'reqformGOPAGE': '',
        'reqformINTEXT': '',
        'reqformNOWPAGE': '',
        'reqformPAGE': 0,
        'reqformrowCount': 20
    }
    content = req.post(url=url, headers=headers, data=params).content.decode('utf-8')
    get_shuangxuan_info(content, redis)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def get_total_num(content):
    soup = BeautifulSoup(content, 'html5lib')
    page_num = re.findall(re.compile('共[0-9]+条'), str(soup))
    page_num = int(page_num[0][1:-1])
    print(page_num)
    return page_num


def parse_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    company_list = soup.find_all(href=re.compile('wszplist2.jsp?'))
    date_list = re.findall(date_pattern, str(soup))
    for i in range(len(company_list)):
        company_name = company_list[i].text.strip()
        date = date_list[i]
        print(company_name, date)
        redis.save_info(table_name, date, company_name)


def get_shuangxuan_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    host = 'http://jobs.ynu.edu.cn/'
    base_url = 'dxzpcontent.jsp?'
    shuangxuan_list = soup.find_all(href=re.compile(base_url))
    for item in shuangxuan_list:
        tail_url = item.attrs['href']
        info = req.get(url=host + tail_url, headers=headers).content.decode('utf-8')
        parse_shuangxuan_info(info, redis)
    pass


def parse_shuangxuan_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    date = re.findall(date_pattern, str(soup))[0]
    company_list = soup.find_all(attrs={'align': 'right'})
    for i in range(1, len(company_list)):
        print(company_list[i].text.strip(), date)
        redis.save_info(table_name, date, company_list[i].text.strip())

if __name__ == '__main__':
    get_ynu_recruitment()

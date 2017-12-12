# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

from util import util

from jedis import jedis

# 新疆大学
table_name = 'xju_company_info'


def get_xju_recruitment():
    base_url = 'http://zsjy.xju.edu.cn/zpxx/'
    first_url = 'http://zsjy.xju.edu.cn/zpxx.htm'
    req = requests.Session()
    redis = jedis.jedis()
    redis.clear_list(table_name)
    headers = util.get_header('zsjy.xju.edu.cn')
    content = req.get(url=first_url, headers=headers).content.decode('utf-8')
    page_num = get_total_page(content)
    parse_info(content, redis)
    headers['Referer'] = first_url
    for i in range(page_num - 1, 0, -1):
        url = base_url + str(i) + '.htm'
        print(url)
        content = req.get(url=url, headers=headers).content.decode('utf-8')
        parse_info(content, redis)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


def get_total_page(content):
    soup = BeautifulSoup(content, 'html5lib')
    total_page = re.findall(re.compile('条  1/[0-9]{2}'), str(soup))
    print(total_page[0][-2:])
    return int(total_page[0][-2:])


def parse_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    company_list = soup.find_all(href=re.compile('info/1980'))
    date_list = soup.select('.timestyle127895')
    for i in range(len(company_list)):
        company_name = company_list[i].text.strip()
        date = date_list[i].text.strip().replace('/', '-')
        if company_name.find('专场') != -1:
            index = company_name.find('】')

            company_name = company_name[index + 1:].strip()
            redis.save_info(table_name, date, company_name)
            print(company_name, date)


if __name__ == '__main__':
    get_xju_recruitment()

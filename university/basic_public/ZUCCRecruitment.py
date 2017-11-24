# coding=utf-8

import re
import requests
from bs4 import BeautifulSoup

# 浙江大学城市学院
from jedis import jedis


def get_zucc_recruit():
    table_name = 'zucc_company_info'
    url = 'http://career.zucc.edu.cn/f/3-moreActivity?activitiesType=CAREER_TALK'
    res = requests.get(url=url).content.decode("utf-8")
    soup = BeautifulSoup(res, 'html5lib')
    redis = jedis.jedis()
    redis.clear_list(table_name)
    company_list = soup.find_all(href=re.compile("activityDetail"))
    date_list = soup.select('.news_date')
    for i in range(0, len(date_list)):
        company_name = company_list[2 * i].text.strip()
        date = date_list[i].text.strip()
        date = date.replace('.', '-')
        print(company_name + date)
        redis.save_info(table_name, date, company_name)
    redis.add_university(table_name)
    redis.add_to_file(table_name)

if __name__ == '__main__':
    get_zucc_recruit()

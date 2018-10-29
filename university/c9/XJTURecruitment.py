import re

import requests
from bs4 import BeautifulSoup

from jedis import jedis


# 宣讲会
def get_data1(page, redis, table_name):
    url = 'http://job.xjtu.edu.cn/listMeeting.do?page=' + str(
        page) + '&filter=%7b%22is4practice%22%3a%22-1%22%2c%22status%22%3a%22-1%22%7d&ext=&sign='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    table_node = soup.find('table', attrs={'class': 'tablerd'})
    trs = table_node.find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        company_name = tds[0].contents[0].text
        date = tds[2].text[:10]
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


# 招聘信息
def get_data2(page, redis, table_name):
    url = 'http://job.xjtu.edu.cn/jobmore.do?page=' + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    node = soup.find('div', attrs={'class': 'jsnr'})
    anchors = node.find_all('a')
    for anchor in anchors:
        company_name = anchor.contents[0].text
        date = anchor.contents[1].text[:10]
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


def get_XJTU_recruit():
    # 西安交通大学

    table_name = 'xjtu_company_info_2018'
    redis = jedis.jedis()
    redis.connect_redis()
    redis.clear_list(table_name)
    # 招聘会
    max_page = 516
    # max_page = 20
    for page in range(1, max_page):
        try:
            get_data1(page, redis, table_name)
            print('page ' + str(page) + ' done!')
        except BaseException as e:
            redis.handle_error(e, table_name)

    # # 招聘信息
    # max_page = 172
    # # max_page = 20
    # for page in range(1, max_page):
    #     try:
    #         get_data1(page, redis, table_name)
    #         print('page ' + str(page) + ' done!')
    #     except BaseException as e:
    #         redis.handle_error(e, table_name)
    # redis.add_to_file(table_name)
    # redis.add_university(table_name)


if __name__ == '__main__':
    get_XJTU_recruit()

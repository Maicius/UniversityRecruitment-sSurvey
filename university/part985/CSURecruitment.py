import requests
import re
from bs4 import BeautifulSoup
import json

from jedis import jedis


data_pattern = re.compile('target="_blank">(.*?)</a>.*?class="spanDate">(.*?)</td>', re.S)
# 匹配括号的模式
pattern = re.compile('[[({【（].*?[]}】）]')


def get_data(typeid):
    # 这个API直接返回公司表单
    url = 'http://jobsky.csu.edu.cn/Home/PartialArticleList'
    form_data1 = {
        'pageindex': 1,
        'pagesize': '10000',
        'typeid': str(typeid),
        'followingdates': '-1',
    }
    response = requests.post(url, form_data1)
    return data_pattern.findall(response.text)


def get_one_page_data(page, redis, table_name):
    data_list = []
    # 根据不同的typeid获取三种招聘信息

    data_list.extend(get_data(1))
    data_list.extend(get_data(2))
    data_list.extend(get_data(3))
    # if page <= 300:
    #     for typeid in range(1, 4):
    #         data_list.extend(get_data(page, typeid))
    # else:
    #     data_list.extend(get_data(page, 1))

    for data in data_list:
        redis.save_dict(table_name, dict(
            company_name=pattern.sub('', data[0]),
            date=data[1].replace('.', '-'),
        ))


def get_csu_recruit():
    # 中南大学
    # 通过改变page_size参数，一次获取所有数据
    # 再通过正则提取
    table_name = 'csu_company_info'
    print(table_name)
    redis = jedis.jedis()
    redis.clear_list(table_name)
    max_page = 2
    for i in range(1, max_page):
        try:
            print("begin")
            get_one_page_data(i, redis, table_name)
            print('Finish All!')
        except Exception as e:
            redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_csu_recruit()

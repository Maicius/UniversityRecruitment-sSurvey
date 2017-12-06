import requests
from bs4 import BeautifulSoup
import json
from jedis import jedis
import datetime
from time import sleep


def get_default_session():
    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'Host': 'scc.cau.edu.cn',
    }
    session.headers.update(header)
    return session


def parse_page(content, redis, table_name):
    soup = BeautifulSoup(content, 'html5lib')
    node_attrs = {
        'class': "newList",
    }
    node = soup.find('ul', attrs=node_attrs)
    if node:
        lis = node.find_all('li')[1:]
        for li in lis:
            company_name = li.find('a').text.strip()
            date = li.find('span').text.strip()[0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def parse_json(content, redis, table_name):
    json_data = json.loads(content)
    if json_data:
        json_data = json_data['data']
        for item in json_data:
            company_name = item['company_name']
            date = item['meet_day']
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_data(page, redis, table_name, s):
    form_data = {
        'pageIndex': str(page),
        'title': '',
        'corporaName': '',
        'province': '',
    }
    url = 'http://scc.cau.edu.cn/recruitmentfair.html/'
    response = s.post(url, form_data)
    content = response.content
    parse_page(content, redis, table_name)


def get_cau_recruitment():
    # 中国农业大学
    table_name = 'CAU_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()
    max_page = 12
    try:
        for i in range(0, max_page):
            get_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_cau_recruitment()

import re
import requests
from bs4 import BeautifulSoup
import json
from jedis import jedis
import datetime
from time import sleep

brackets_pattern = re.compile('[[({【（].*?[]}】）]')


def get_default_session():
    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    return session


def parse_page(content, redis, table_name):
    soup = BeautifulSoup(content, 'html5lib')
    node_attrs = {
        'class': "infoBox mt10",
    }
    node = soup.find('div', attrs=node_attrs)
    if node:
        uls = node.find_all('ul')[1:-2]
        for ul in uls:
            lis = ul.find_all('li')
            company_name = lis[0].find('a').text.strip()
            date = lis[4].text[0:10]
            if date.find('取消') == -1:
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
            # print(company_name)
            # print(date)
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_data(page, redis, table_name, s):
    url = 'http://jiuye.lut.cn/module/getcareers?start=%d&count=16&keyword=&address=&professionals=&career_type=&type=inner&day=' % page
    response = s.get(url)
    content = response.content
    parse_json(content, redis, table_name)


def get_lut_recruitment():
    # 兰州理工大学
    table_name = 'lut_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()

    max_page = 300
    try:
        for i in list(range(0, max_page))[0::15]:
            get_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
            sleep(1)
    except Exception as e:
        redis.handle_error(e)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_lut_recruitment()

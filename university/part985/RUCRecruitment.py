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
    }
    session.headers.update(header)
    return session


def parse_page(content, redis, table_name):
    soup = BeautifulSoup(content, 'html5lib')
    node_attrs = {
        'class': "list",
    }
    node = soup.find('div', attrs=node_attrs)
    if node:
        ps = node.find_all('p')
        for p in ps:
            spans = p.find_all('span')
            company_name = spans[0].text.strip()
            date = spans[1].text.strip()
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
    url = 'http://rdjy.ruc.edu.cn/cms/meeting/?page=%d' % page
    response = s.get(url)
    content = response.content
    parse_page(content, redis, table_name)


def get_ruc_recruitment():
    # 中国人民大学
    table_name = 'ruc_company_info'

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
    get_ruc_recruitment()

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
        json_data = json.loads(content)['info']
        for item in json_data:
            company_name = item['title']
            date = item['held_date']
            if company_name.find(u'宣讲会') == -1:
                continue
            company_name = brackets_pattern.sub('', company_name)
            # print(company_name)
            # print(date)
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_data(page, redis, table_name, s):
    url = 'http://yangtzeu.91wllm.com/teachin/index?page=%d' % page
    response = s.get(url)
    content = response.content
    parse_page(content, redis, table_name)


def get_yangtzeu_recruitment():
    # 长江大学
    table_name = 'yangtzeu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()

    max_page = 18
    try:
        for i in range(1, max_page):
            get_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_yangtzeu_recruitment()

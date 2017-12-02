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
        'height': "707",
        'align': "center",
    }
    node = soup.find('td', attrs=node_attrs)
    if node:
        tables = node.find_all('table')[1:]
        for table in tables:
            company_name = table.find('a').text.strip()
            date = table.find('td', attrs={'class': 'p12hui2'}).text[0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def parse_json(content, redis, table_name):
    json_data = json.loads(content)
    if json_data:
        for item in json_data:
            company_name = item['title']
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=str(),
            ))
    else:
        pass


def get_data(page, redis, table_name, s):
    url = 'http://job.imu.edu.cn/JobInfo/JobZPList/41?PageIndex=%d' % page
    response = s.get(url)
    content = response.content
    parse_page(content, redis, table_name)


def get_lmu_recruitment():
    # 内蒙古大学
    table_name = 'lmu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()
    max_page = 36
    try:
        for i in range(1, max_page):
            get_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_lmu_recruitment()

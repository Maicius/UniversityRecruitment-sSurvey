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

    }
    node = soup.find('table', attrs=node_attrs)
    if node:
        trs = node.find('tbody').find_all('tr')[:-1]
        for tr in trs:
            tds = tr.find_all('td')
            company_name = tds[1].find('a', target='_blank').text.strip()
            date = tds[2].text.strip()[1:11]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def parse_json(content, redis, table_name, date):
    json_data = json.loads(content)
    if json_data:
        for item in json_data:
            company_name = item['title']
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=str(date),
            ))
    else:
        pass


def get_data(date, redis, table_name, s):
    url = 'http://202.118.65.2/app/portals/recruiterNews?date=' + date.strftime('%Y-%m-%d')
    response = s.get(url)
    content = response.content
    parse_json(content, redis, table_name, date)


def get_dlut_recruitment():
    # 大连理工大学
    table_name = 'dlut_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()
    begin_date = datetime.date(2017, 10, 1)
    end_date = datetime.date.today()
    try:
        while begin_date != end_date:
            get_data(begin_date, redis, table_name, session)
            print(str(begin_date) + ' done!')
            begin_date += datetime.timedelta(days=1)
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_dlut_recruitment()

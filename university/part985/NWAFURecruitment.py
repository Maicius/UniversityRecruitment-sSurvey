import requests
from bs4 import BeautifulSoup
import json
from jedis import jedis
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


def parse_json(content, redis, table_name):
    json_data = json.loads(content)['rows']
    if json_data:
        for row in json_data:
            company_name = row['CompanyName']
            date = row['MeetDate'][0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_data(page, redis, table_name, s):
    url = 'http://jyglxt.nwsuaf.edu.cn/Frame/Data/jdp.ashx?rnd=1511946466074&fn=GetJobFairList&StartDate=2000-01-01&InfoState=1&start=%d&limit=100&CompanyKey=' % page
    response = s.get(url)
    content = response.content
    parse_json(content, redis, table_name)


def get_nwafu_recruitment():
    # 西北农林科技大学
    table_name = 'nwafu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = get_default_session()
    max_page = 2000
    i = 0
    try:
        while i <= 2000:
            get_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
            i += 100
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_nwafu_recruitment()

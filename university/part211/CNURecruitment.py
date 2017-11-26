import requests
from bs4 import BeautifulSoup
from jedis import jedis
import json


def get_one_page_data(page, redis, table_name, s):
    url = 'http://xsjyc.chd.edu.cn/Frame/Data/jdp.ashx?rnd=1511684506710&fn=GetJobFairList&StartDate=2000-01-01&InfoState=1&start=%d&limit=100&CompanyKey=' % page
    response = s.get(url)
    json_data = json.loads(response.text)
    if json_data:
        rows = json_data.get('rows', None)
        if rows:
            for row in rows:
                company_name = row['CompanyName']
                date = row['MeetDate'][0:10]
                redis.save_dict(table_name, dict(
                    company_name=company_name,
                    date=date,
                ))


def get_cau_recruitment():
    # 长安大学
    table_name = 'cau_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 4100
    i = 0
    try:
        while i <= max_page:
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
            i += 100
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_cau_recruitment()

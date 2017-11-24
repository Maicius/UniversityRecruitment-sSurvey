import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep
import re

pattern = re.compile('[[({【（].*?[]}】）]')


def get_one_page_data(page, redis, table_name, s):
    url = 'http://bys.hqu.edu.cn/zpzl/xyxj/' + str(page) + '.htm'
    response = s.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    node = soup.find('table', attrs={'width': "100%", 'border': "0", 'cellpadding': "0", 'cellspacing': "0"})
    if node:
        trs = node.find('tbody').find_all('tr')
        for tr in trs[7:]:
            tds = tr.find_all('td')
            company_name = tds[0].find('a').text.strip()
            company_name = pattern.sub('', company_name)
            date = tds[3].text.strip()[0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))

    else:
        pass


def get_hqu_recruitment():
    # 华侨大学
    table_name = 'hqu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 42
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_hqu_recruitment()

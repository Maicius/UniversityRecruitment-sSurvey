import requests
from bs4 import BeautifulSoup
from jedis import jedis
import re

date_pattern = re.compile('[(（].*?[）)]')


def get_one_page_data(page, redis, table_name):
    url = 'http://job.tjpu.edu.cn/zph?currentPage=' + str(page) + '&totalPage=153&type=12'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    node = soup.find('div', id='bxzph')
    divs = node.find_all('div', attrs={'class': 'mulu_1'})
    for div in divs:
        date = div.find('div', attrs={'class': 'date'}).text.strip()
        text = div.find('div', attrs={'class': 'biaoti'}).text.strip()
        company_name = date_pattern.sub('', text)
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


def get_tjpu_recruitment():
    # 天津工业大学
    table_name = 'tjpu_company_info'
    redis = jedis.jedis()
    redis.clear_list(table_name)

    max_page = 153
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_tjpu_recruitment()

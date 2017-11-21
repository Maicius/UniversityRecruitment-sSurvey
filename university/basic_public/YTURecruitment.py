import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep
import re

date_pattern = re.compile('举办日期：(.*?)\n', re.S)


def get_one_page_data(page, redis, table_name):
    url = 'http://career.ytu.edu.cn/jobfair/jobfair-list.php?page=' + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    divs = soup.find_all('div', attrs={'class': 'center link_bk'})
    for div in divs:
        anchor = div.find('a')
        company_name = anchor.contents[0].text if anchor.contens else anchor.text

        date = date_pattern.findall(div.text)[0]
        # 格式化日期
        format_date = []
        for i in date[0:-1]:
            if i.isdigit():
                format_date.append(i)
            else:
                format_date.append('-')
        format_date = ''.join(format_date)

        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=format_date,
        ))


def get_ytu_recruitment():
    # 烟台大学
    table_name = 'ytu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    max_page = 105
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
            sleep(0.2)
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_ytu_recruitment()

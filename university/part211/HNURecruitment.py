import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep

# 海南大学
def get_one_page_data(page, redis, table_name, s):
    url = 'http://www.hainu.edu.cn/stm/jiuye/SHTML_liebiao.asp@bbsid=3875&pa=%d.shtml' % page
    response = s.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    node = soup.find('ul', attrs={'class': 'v105 hang0'})
    if node:
        lis = node.find_all('li')
        for li in lis:
            company_name = li.find('a').find('b').text.strip()
            date = li.find('span').text[6:15].strip().replace('/', '-')
            if date.find('1900') == -1:
                redis.save_dict(table_name, dict(
                    company_name=company_name,
                    date=date,
                ))
    else:
        pass


def get_hnu_recruitment():

    table_name = 'hnu1_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 7

    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_hnu_recruitment()

import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name, s):
    url = 'http://bkjyw.swu.edu.cn/s/bkjy/xyzp/index_%d.html' % page
    response = s.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    node = soup.find('ul', attrs={'id': 'cnt_lst'})
    if node:
        lis = node.find_all('li')
        for li in lis:
            company_name = li.find('a').text.strip()
            # 去除时间
            company_name = company_name[company_name.find('/')+1:]
            date = li.find('span', attrs={'class': 'rt'}).text.strip()
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_swu_recruitment():
    # 西南大学
    table_name = 'swu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 97
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_swu_recruitment()

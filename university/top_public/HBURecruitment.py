import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name, s):
    url = 'http://job.hbu.cn/index.php/gggs.html?&p=' + str(page)
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    node = soup.find('ul', attrs={'class': "textlist1"})
    if node:
        lis = node.find_all('li')
        for li in lis:
            company_name = li.find('a', target='_blank').text.strip()
            date = li.find('span').text.strip()[0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_hbu_recruitment():
    # 河北大学
    table_name = 'hbu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 20
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_hbu_recruitment()

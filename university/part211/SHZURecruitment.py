import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name, s):
    url = 'http://zjc.shzu.edu.cn/6193/list%d.htm' % page
    response = s.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    node = soup.find('div', attrs={'id': 'wp_news_w9'})
    if node:
        companies_name = list(map(lambda x: x.text.strip(), node.find_all('a', attrs={'target': '_blank'})))
        dates = list(map(lambda x: x.text.strip(), node.find_all('span', attrs={'style': 'text-align:right;float:right;'})))
        for i in range(len(companies_name)):
            redis.save_dict(table_name, dict(
                company_name=companies_name[i],
                date=dates[i],
            ))
    else:
        pass


def get_shzu_recruitment():
    # 石河子大学
    table_name = 'shzu_company_info'

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
    get_shzu_recruitment()

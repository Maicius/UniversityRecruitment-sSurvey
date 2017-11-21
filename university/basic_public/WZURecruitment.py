import requests
from bs4 import BeautifulSoup
from jedis import jedis


def get_one_page_data(page, redis, table_name):
    url = 'http://job.wzu.edu.cn/teachin/index?domain=wzu&page=' + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    uls = soup.find_all('ul', attrs={'class': 'infoList teachinList'})
    for ul in uls:
        lis = ul.find_all('li')
        company_name = lis[0].contents[0].text
        date = lis[4].text[0:10]
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


def get_wzu_recruitment():
    # 温州大学
    table_name = 'wzu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    max_page = 24
    try:
        for i in range(0, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_wzu_recruitment()

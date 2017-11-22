import requests
from bs4 import BeautifulSoup
from jedis import jedis


def get_one_page_data(page, redis, table_name):
    url = 'http://jdjy.jhun.edu.cn/teachin/index?domain=jhun&page=' + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    list_node = soup.find('div', attrs={'class': 'infoBox mt10'})
    uls = list_node.find_all('ul', attrs={'class': 'infoList teachinList'})
    for ul in uls:
        lis = ul.find_all('li')
        anchor = lis[0].find('a')
        if anchor:
            company_name = anchor.text.strip()
            date = lis[4].text[0:10]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
        else:
            pass


def get_jhu_recruitment():
    # 江汉大学
    table_name = 'jhu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    max_page = 19
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_jhu_recruitment()

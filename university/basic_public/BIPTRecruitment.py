import requests
from bs4 import BeautifulSoup
from jedis import jedis


def get_one_page_data(page, redis, table_name):
    url = 'http://jobbipt.jysd.com/teachin?title=&range=0&city=&time=0&page=' + str(page)
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


def get_bipt_recruitment():
    # 北京石油化工学院
    table_name = 'bipt_company_info'
    print("北京石油化工学院开始================================")
    redis = jedis.jedis()
    redis.clear_list(table_name)
    # 只有一页.....
    max_page = 2
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
    except BaseException as e:
        redis.handle_error(e, table_name)
        pass
    redis.add_to_file(table_name)
    redis.add_university(table_name)
    print("北京石油化工学院Finish================================")


if __name__ == '__main__':
    get_bipt_recruitment()

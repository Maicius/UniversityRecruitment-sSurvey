import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name):
    url = 'http://njupt.91job.gov.cn/teachin/index?page=' + str(page)
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
            # print(company_name)
            # print(date)
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
        else:
            pass


def get_njupt_recruitment():
    # 南京邮电大学
    table_name = 'njupt_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    max_page = 59
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name)
            print('page ' + str(i) + ' done!')
            sleep(0.5)

    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_njupt_recruitment()

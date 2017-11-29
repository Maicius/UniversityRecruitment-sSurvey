import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name, s):
    url = 'http://career.buaa.edu.cn/getJobfairAllInfoAction.dhtml?more=all&pageIndex=%d&selectedNavigationName=RecruitmentInfoMain&selectedItem=jobFair' % page
    response = s.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    node = soup.find('table', attrs={'class': 'info_table', 'style': 'border-collapse:collapse;'})
    if node:
        trs = node.find_all('tr')
        for tr in trs:
            company_name = tr.find('a').text.strip()
            date = tr.find('td', attrs={'class': 'info_right', 'valign': 'top'}).text.strip()
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_bhu_recruitment():
    # 北京航空航天大学
    table_name = 'bhu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 87
    try:
        for i in range(1, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_bhu_recruitment()

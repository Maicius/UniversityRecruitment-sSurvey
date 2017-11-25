import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_page_data(page, redis, table_name, s):
    url = 'http://www.91.wust.edu.cn/MeetList.aspx?pageId=' + str(page)
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    node = soup.find('table', attrs={'style': "width:762px; border-top:solid 1px  #CCCCCC;"})
    if node:
        trs = node.find('tbody').find_all('tr')[:-1]
        for tr in trs:
            tds = tr.find_all('td')
            company_name = tds[1].find('a', target='_blank').text.strip()
            date = tds[2].text.strip()[1:11]
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        pass


def get_wust_recruitment():
    # 武汉科技大学
    table_name = 'wust_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    max_page = 180
    try:
        for i in range(0, max_page):
            get_one_page_data(i, redis, table_name, session)
            print('page ' + str(i) + ' done!')
    except Exception as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_wust_recruitment()

import requests
from bs4 import BeautifulSoup
from jedis import jedis
import re


def get_data(table_name, redis):
    pattern = re.compile('[[({【（].*?[]}】）]')
    url = 'http://career.shcc.edu.cn/Meeting.asp'
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
    trs = soup.find('div', attrs={'class': 'coninfo_left'}).find_all('tr')[1:6]
    for tr in trs:
        tds = tr.find_all('td')
        company_name = pattern.sub('', tds[1].contents[0].text)
        date = tds[2].contents[0].text[5:]
        print(company_name + date)
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


def get_scc_recuit():
    # 上海海关学院
    table_name = 'scc_company_info'
    redis = jedis.jedis()
    redis.clear_list(table_name)
    # 只有一页
    get_data(table_name, redis)

    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_scc_recuit()

# coding=utf-8
import requests
from bs4 import BeautifulSoup
from jedis import jedis


# 华中科技大学校招信息
def get_data(page, re, table_name):
    s = requests.session()
    response = s.get('http://job.hust.edu.cn/searchJob_%d.jspx?fbsj=&sdate=&edate=&q=&type=0' % page)

    soup = BeautifulSoup(response.text, 'lxml')

    # 找到招聘会节点
    node = soup.find_all('table', attrs={'cellpadding': '4', 'cellspacing': '0', 'class': 'fdhy_tb002'})[1]

    trs = node.find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        company_name = tds[0].find('a')['title']
        date = tds[1].find('span').text[0:10]
        # py2
        # company_name = tds[0].find('a')['title'].encode('utf-8')
        # date = tds[1].find('span').text[0:10].encode('utf-8')
        re.save_dict(table_name, dict(company_name=company_name,
                                      date=date))


def get_cqu_recruit():
    table_name = 'HUST_company_info'
    re = jedis.jedis()
    max_page = 212
    try:
        # 从第三页开始爬取
        for i in range(3, max_page):
            get_data(i, re, table_name)
            print('page ' + str(i) + ' done!')
    except BaseException, e:
        re.handle_error(e, table_name)
    re.add_to_file(table_name)
    re.add_university(table_name)


if __name__ == '__main__':
    get_cqu_recruit()

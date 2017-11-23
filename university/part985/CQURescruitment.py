# coding=utf-8
import requests
from bs4 import BeautifulSoup
from jedis import jedis


# python 2
# sudo pip install lxml
# python 3
# sudo pip3 install lxml
# 重庆大学校招信息
def get_data(url, page, re, table_name):
    form_data = {
        'zphlx': '1',
        'jbdwmc': '',
        'zphrq': '',
        'zphcdmc': '',
        'pages.pageSize': '30',
        'pages.currentPage': str(page),
        'pages.maxPage': '116',
        'pageno': '',
    }
    response = requests.post(url, data=form_data)
    content = response.text
    soup = BeautifulSoup(content, 'html5lib')
    trs = soup.find('div', attrs={'class': 'result_con'}).find('table', attrs={'width': '960'}).find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        # py2
        # re.save_dict(table_name, dict(company_name=tds[0].find('a').text.strip().encode('utf-8'),
        #                               date=tds[3].text.strip().encode('utf-8')[0:10]))
        # for py3
        re.save_dict(table_name, dict(company_name=tds[0].find('a').text.strip(),
                                      date=tds[3].text.strip()[0:10]))


def get_cqu_recruit():
    table_name = 'cqu_company_info'
    re = jedis.jedis()
    re.clear_list(table_name)
    url = 'http://www.job.cqu.edu.cn/jyxt/zczphxxlistlogin.do'
    max_page = 124
    try:
        for i in range(1, max_page):
            get_data(url, i, re, table_name)
            print('page ' + str(i) + ' done!')
    except BaseException as e:
        re.handle_error(e, table_name)
    re.add_to_file(table_name)
    re.add_university(table_name)


if __name__ == '__main__':
    get_cqu_recruit()

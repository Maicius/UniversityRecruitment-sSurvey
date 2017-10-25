import requests
from bs4 import BeautifulSoup
from Util import Util

# 获取浙江大学就业数据
def get_zju_rescruit():
    table_name = "zju_company_info"
    base_url = "http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do"
    params = {'zphix': 0, 'dwmc': '', 'hylb': '', 'zphrq': '', 'pages.pageSize': 30, 'pages.currentPage': 0,
              'pages.maxPage': 17, 'pageno': ''}
    req = requests.Session()
    re = Util.jedis()
    re.connect_redis()
    for i in range(1, 19):
        params['pages.currentPage'] = i
        res = req.post(base_url, data=params)
        content = res.content.decode("GBK")
        # print(content)
        parse_info(content, re, table_name)
    re.add_to_file(table_name)
    re.add_university(table_name)


def parse_info(content, re, table_name):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("td")
    try:
        for i in range(11, 130, 4):
            company_name = company_list[i].text.strip()
            date = company_list[i + 2].text.strip()[0:10]
            # 过滤掉已经被取消掉宣讲会
            if company_name.find("已取消") == -1:
                re.save_info(table_name, date, company_name)
                print(company_name)
                print(date)
    except IndexError:
        print("finish")
    except ConnectionError as e:
        re.handle_error(e, table_name)


if __name__ == '__main__':

    get_zju_rescruit()
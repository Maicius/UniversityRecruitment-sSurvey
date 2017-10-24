import requests
from bs4 import BeautifulSoup
from Util import Util

def get_zju_rescruit():
    base_url = "http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do"
    params = {'zphix': 0, 'dwmc': '', 'hylb': '', 'zphrq': '', 'pages.pageSize': 30, 'pages.currentPage': 0,
              'pages.maxPage': 17, 'pageno': ''}
    req = requests.Session()
    re = Util.jedis()
    re.connect_redis()
    for i in range(1, 18):
        params['pages.currentPage'] = i
        res = req.post(base_url, data=params)
        content = res.content.decode("GBK")
        # print(content)
        parse_info(content, re)


def parse_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("td")
    for i in range(11, 130, 4):
        company_name = company_list[i].text.strip()
        date = company_list[i + 2].text.strip()[0:10]
        print(company_name)
        print(date)
        re.save_info("zju_company_info", date, company_name)


if __name__ == '__main__':
    get_zju_rescruit()
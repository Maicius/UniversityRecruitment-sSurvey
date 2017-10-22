# coding = utf-8
import requests
from bs4 import BeautifulSoup
from Util import connect_redis, get_header


# 获取四川大学宣讲会信息
def get_scu_recruit():
    host = 'jy.scu.edu.cn'
    first_url = "http://jy.scu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx"
    base_url = "http://jy.scu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
    re = connect_redis()
    req = requests.Session()
    scu_header = get_header(host)
    res = req.get(headers=scu_header, url=first_url)
    content = res.content.decode("utf-8")
    parse_scu(content, re)
    for i in range(1, 224):
        url = base_url + str(i)
        res = req.get(headers=scu_header, url=url)
        content = res.content.decode("utf-8")
        parse_scu(content, re)


def parse_scu(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_info = soup.find_all('li')
    for num in range(8, 28):
        # print(company_info[num].text)
        company = company_info[num].text
        # company_name = company[2]
        # company_date = company[4]
        print(company)
        re.lpush("scu_company_info", company)




# coding = utf-8
import requests
from bs4 import BeautifulSoup
from Util import connect_redis, get_header


def get_nju_rescruit():
    base_url = "http://job.nju.edu.cn/login/nju/home.jsp?type=zph&DZPHBH=&sfss=sfss&zphzt=&jbksrq=&jbjsrq=&sfgq=&pageSearch=2&pageNow="
    req = requests.Session()
    header = get_header("job.nju.edu.cn")
    re = connect_redis()
    for i in range(1, 118):
        print(i)
        content = req.get(headers=header, url=base_url + str(i)).content.decode("utf-8")
        parse_nju_info(content, re)
    print("finish")


def parse_nju_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("li")
    length = len(company_list)
    print(length)
    for i in range(12, length):
        try:
            info = {"company": company_list[i].text}
            re.lpush("nju_company_info", info)
        except IndexError:
            print(company_list[i].text)
            continue

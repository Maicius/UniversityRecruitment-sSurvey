# coding = utf-8
import requests
from bs4 import BeautifulSoup

from Util import Util


def get_nju_rescruit():
    base_url = "http://job.nju.edu.cn/login/nju/home.jsp?type=zph&DZPHBH=&sfss=sfss&zphzt=&jbksrq=&jbjsrq=&sfgq=&pageSearch=2&pageNow="
    req = requests.Session()
    header = Util.get_header("job.nju.edu.cn")
    re = Util.jedis()
    re.connect_redis()
    for i in range(1, 118):
        print(i)
        content = req.get(headers=header, url=base_url + str(i)).content.decode("utf-8")
        parse_nju_info(content, re)
    re.add_university("nju_company_info")
    print("finish")


def parse_nju_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("li")
    length = len(company_list)
    print(length)
    for i in range(12, length):
        try:
            info = company_list[i].text.split("\n")
            company_name = info[3].split("\t")[1].strip()
            date = info[5].strip().split("\xa0\xa0")
            re.save_info("nju_company_info", date, company_name)
        except IndexError:
            print(company_list[i].text)
            continue

if __name__ == '__main__':
    get_nju_rescruit()
# coding = utf-8
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


# 获取南京大学数据
def get_nju_rescruit():
    print("NJU Begin===================================================")
    base_url = "http://job.nju.edu.cn/login/nju/home.jsp?type=zph&DZPHBH=&sfss=sfss&zphzt=&jbksrq=&jbjsrq=&sfgq=&pageSearch=2&pageNow="
    req = requests.Session()
    header = util.get_header("job.nju.edu.cn")
    re = jedis.jedis()
    re.connect_redis()
    for i in range(1, 118):
        print(i)
        content = req.get(headers=header, url=base_url + str(i)).content.decode("utf-8")
        parse_nju_info(content, re)
    re.add_university("nju_company_info")
    re.add_to_file("nju_company_info")
    print("NJU finish ===================================================")


def parse_nju_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("li")
    length = len(company_list)
    for i in range(12, length):
        try:
            info = company_list[i].text.split("\n")
            company_name = info[3].split("\t")[1].strip()
            date = info[5].strip().split("\xa0\xa0")
            print("南京大学" + company_name)
            re.save_info("nju_company_info", date, company_name)
        except IndexError:
            print("error:" + company_list[i].text)
            continue


if __name__ == '__main__':
    get_nju_rescruit()

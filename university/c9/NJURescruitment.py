# coding = utf-8
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


table_name = "nju_company_info_2018"


# 获取南京大学数据
def get_nju_rescruit():
    print("NJU Begin===================================================")
    base_url = "http://job.nju.edu.cn:9081/login/nju/home.jsp?type=zph&DZPHBH=&sfss=sfss&zphzt=&jbksrq=&jbjsrq=&sfgq=&pageSearch=2&pageNow="
    req = requests.Session()
    header = util.get_header("job.nju.edu.cn")
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    for i in range(1, 120):
        print(i)
        content = req.get(headers=header, url=base_url + str(i)).content.decode("utf-8")
        parse_nju_info(content, re)
    get_zph_info(req, header, re)
    re.add_university(table_name)
    re.add_to_file(table_name)
    print("NJU finish ===================================================")


# 获取大型招聘会的信息
def get_zph_info(req, header, re):
    base_url = "http://job.nju.edu.cn:9081/login/nju/home.jsp?type=dw&DZPHBH=61or8m5y-vn4s-kqae-zahn-zp4epxsp0mt4&pageNow="
    for i in range(1, 10):
        url = base_url + str(i)
        print("专场招聘会:" + str(i))
        content = req.get(headers=header, url=url).content.decode("utf-8")
        parse_zph_info(content, re)


def parse_zph_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("li")
    for item in company_list:
        info = item.text.split("\n")
        company_name = info[3].strip()
        date = "2017-11-25"
        re.save_info(table_name, date, company_name)


def parse_nju_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("li")
    length = len(company_list)
    for i in range(12, length):
        try:
            info = company_list[i].text.split("\n")
            company_name = info[3].split("\t")[1].strip()
            if company_name.find('澳门国际银行股份有限公司') != -1:
                company_name = '澳门国际银行股份有限公司'
            time = info[5].strip().split("\xa0\xa0")
            if len(time) == 3:
                date = time[1]
            else:
                date = time[0]
            print("南京大学:" + date + "\t" + company_name)
            re.save_info(table_name, date, company_name)
        except IndexError:
            print("error:" + company_list[i].text)
            continue


if __name__ == '__main__':
    get_nju_rescruit()

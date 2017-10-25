import requests
from bs4 import BeautifulSoup

from Util import Util


# 华北电力大学
# 包括宣讲会与双选会
def get_ncepu_recruit():
    table_name = "ncepu_table_name"
    base_url = "http://job.ncepu.edu.cn/teachin/index?domain=ncepu&page="
    req = requests.Session()
    re = Util.jedis()
    re.connect_redis()
    host = "job.ncepu.edu.cn"
    header = Util.get_header(host)
    # 获取宣讲会信息
    for i in range(1, 30):
        res = req.get(headers=header, url=base_url + str(i))
        html = res.content.decode("utf-8")
        parse_info(html, re, table_name)
    re.add_university(table_name)
    re.add_to_file(table_name)


def parse_info(html, re, table_name):
    soup = BeautifulSoup(html, "html5lib")
    company_list = soup.find_all("ul")
    print(company_list)
    try:
        for j in range(3, 24):
            infos = company_list[j].text.split("\n")
            company_name = infos[1].strip()
            date = infos[5].strip()[0:10]
            print(company_name)
            print(date)
            re.save_info(table_name, date, company_name)
    except IndexError:
        print("finish")
    except ConnectionError as e:
        re.handle_error(e, table_name)


if __name__ == '__main__':
    get_ncepu_recruit()
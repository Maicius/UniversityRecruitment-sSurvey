# coding = utf-8
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


# 获取兰州大学信息
def get_lzu_rescruit():
    base_url = "http://job.lzu.edu.cn/htmlfile/article/list/119/list_"
    url_tail = ".shtml"
    host = "job.lzu.edu.cn"
    header = util.get_header(host)
    max_page_num = 50
    req = requests.Session()
    re = jedis.jedis()
    re.connect_redis()
    for i in range(1, max_page_num + 1):
        url = base_url + str(i) + url_tail
        html = req.get(headers=header, url=url).content.decode("utf-8")
        parse_html(html, re)
        print(i)
    re.add_university("lzu_company_info")
    print("finish")


def parse_html(html, re):
    soup = BeautifulSoup(html, "html5lib")
    company_list = soup.find_all("li")
    for i in range(24, 78):
        try:
            text = company_list[i].text
            if text != ' ':
                date = text[1: 11]
                company = text[12:]
                re.save_info("lzu_company_info", date, company)
        except IndexError:
            print("Error:" + str(len(company_list)))
            continue

if __name__ == "__main__":
    get_lzu_rescruit()
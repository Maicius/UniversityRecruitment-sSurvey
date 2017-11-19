# coding = utf-8

import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


table_name = "company_info"
def get_China_top500():
    base_url = "http://www.fortunechina.com/search/f500beta/search.do?facetAction=&facetStr=type%23%E6%89%80%E5%B1%9E%E6%A6%9C%E5%8D%95%23%E4%B8%AD%E5%9B%BD500%E5%BC%BA%3B&sort=1&key=&curPage="
    page_num = 83
    get_top_500(base_url, page_num, "ChinaTop500")
    print("finish")


def get_world_top500():
    base_url = "http://www.fortunechina.com/search/f500beta/search.do?facetAction=&facetStr=type%23%E6%89%80%E5%B1%9E%E6%A6%9C%E5%8D%95%23%E4%B8%96%E7%95%8C500%E5%BC%BA%3B&sort=1&key=&curPage="
    page_num = 74
    get_top_500(base_url, page_num, "WorldTop500")
    print("finish")


def get_usa_top500():
    base_url = "http://www.fortunechina.com/search/f500beta/search.do?facetAction=a%23type%23%E7%BE%8E%E5%9B%BD500%E5%BC%BA&facetStr=&sort=1&key=&curPage="
    page_num = 64
    get_top_500(base_url, page_num, "USATop500")
    print("finish")


def get_top_500(base_url, page_num, company_type):
    host = "www.fortunechina.com"
    header = util.get_header(host)
    req = requests.Session()
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    for i in range(1, page_num):
        url = base_url + str(i)
        print(i)
        res = req.get(headers=header, url=url).content.decode("utf-8")
        parse_top500(res, re, company_type)
    re.add_to_file_tail(table_name)


def parse_top500(content, re, company_type):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("span")
    company_index = []
    for i in range(len(company_list)):
        if company_list[i].text.find("500强] 2017年") != -1:
            company_index.append(i)
            try:
                index = i
                company_rank = company_list[index].text.strip()
                company_name = company_list[index + 1].text.strip()
                company_industry = company_list[index + 4].text.strip()
                company_contry = company_list[index + 6].text.strip()
                company_profit = company_list[index + 8].text.strip()
                company_people_num = company_list[index + 10].text.strip()
                company_type = company_type

                # 替换company_name中的特殊符号
                company_name = company_name.replace('\'', '==')
                re.save_company_info(table_name, company_rank, company_name, company_industry, company_contry,
                                     company_profit, company_people_num, company_type)
            except IndexError:
                print(len(company_list))
                continue

if __name__ == "__main__":
    get_China_top500()
    get_world_top500()
    get_usa_top500()

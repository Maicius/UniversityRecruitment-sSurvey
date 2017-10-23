# coding = utf-8

import requests
from bs4 import BeautifulSoup
from Util import Util

def get_China_top500():
    base_url = "http://www.fortunechina.com/search/f500beta/search.do?facetAction=&facetStr=type%23%E6%89%80%E5%B1%9E%E6%A6%9C%E5%8D%95%23%E4%B8%AD%E5%9B%BD500%E5%BC%BA%3B&sort=1&key=&curPage="
    host = "www.fortunechina.com"
    header = Util.get_header(host)
    req = requests.Session()
    re = Util.jedis()
    re.connect_redis()
    for i in range(1, 83):
        url = base_url + str(i)
        print(i)
        res = req.get(headers=header, url=url).content.decode("utf-8")
        parse_China_top500(res, re)

def parse_China_top500(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all("span")

    for i in range(12, 152, 14):
        try:
            index = i
            company_rank = company_list[index].text.strip()
            company_name = company_list[index + 1].text.strip()
            company_industry = company_list[index + 4].text.strip()
            company_contry = company_list[index + 6].text.strip()
            company_profit = company_list[index + 8].text.strip()
            company_people_num = company_list[index + 10].text.strip()
            company_type = "ChinaTop500"
            re.save_company_info("company_info", company_rank, company_name, company_industry, company_contry, company_profit, company_people_num, company_type)
        except IndexError:
            print(len(company_list))
            continue


if __name__ == "__main__":
    get_China_top500()
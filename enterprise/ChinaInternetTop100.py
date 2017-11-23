# coding=utf-8
import requests

from jedis import jedis
from bs4 import BeautifulSoup

table_name = "it_top_100_company_info"
def get_it_top100():
    url = "http://www.sohu.com/a/162100864_608782"
    req = requests.Session()
    re = jedis.jedis()
    re.clear_list(table_name)
    res = req.get(url=url)
    content = res.content.decode("utf-8")
    parse_info(content, re)


def parse_info(content, re):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all('tr')
    for i in range(1, 100):
        infos = company_list[i].text.split("\n")
        company_name = infos[2].strip()
        short_name = infos[3].strip()
        product = infos[4].strip()
        re.save_dict(table_name, data=dict(company_name=company_name, short_name=short_name, product=product))
    re.add_to_file_tail(table_name)
    print("中国IT企业100强获取完成")

if __name__ == '__main__':
    get_it_top100()
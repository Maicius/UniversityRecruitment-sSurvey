#coding=utf-8
import requests

from util import util
from jedis import jedis
from bs4 import BeautifulSoup

table_name = "fdu_company_info"


# 复旦大学
def get_fdu_rescruit():
    host = "www.career.fudan.edu.cn"
    headers = util.get_header(host)
    headers['cookie'] = 'JSESSIONID=0000qZlE0QPPNarjW8SKyrjJPEW:19b14rm85'
    # 将count掉值设置为大于等于总信息的数字，可以一次性获得所有数据
    url = "http://www.career.fudan.edu.cn/jsp/career_talk_list.jsp?count=3000&list=true"
    req = requests.Session()
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    res = req.get(headers=headers, url=url)
    content = res.content.decode("utf-8")
    parse_info(content, re)
    re.add_university(table_name)
    re.add_to_file(table_name)


def parse_info(content, re):
    # print(content)
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all(id='tab1_bottom')
    for item in company_list:
        company_name = item.select('.tab1_bottom1')[0].string
        date = item.select('.tab1_bottom3')[0].string
        # 有部分数据为空，仅有[已举办字样]，需过滤
        if len(company_name) > 5:
            re.save_info(table_name, date, company_name)
    print("finish")


if __name__ == '__main__':
    get_fdu_rescruit()
import re
import requests

from jedis import jedis
from util import util
from bs4 import BeautifulSoup

table_name = "scut_company_info"
pattern = re.compile('[0-9]+-[0-9][0-9]-[0-9][0-9]')

# 华南理工大学
def get_scut_recuit():
    print("开始获取华南理工大学数据=====================")
    url = "http://jyzx.6ihnep7.cas.scut.edu.cn/jyzx/xs/zpxx/xyxj/"

    req = requests.Session()

    headers = util.get_header(host='jyzx.6ihnep7.cas.scut.edu.cn')
    redis = jedis.jedis()
    redis.clear_list(table_name)
    for i in range(1, 65):
        try:
            data = {'pageNo': '60', 'daoxv1': '0', 'entName': '', 'time': '-1', 'pageNO': str(i)}
            content = req.post(url=url, headers=headers, data=data).content.decode('utf-8')
            parse_info(redis, content)
        except BaseException as e:
            util.format_err(e)
            break
    redis.add_to_file(table_name)
    redis.add_university(table_name)
    print("获取华南理工大学数据完成=======================")


def parse_info(redis, content):
    soup = BeautifulSoup(content, 'html5lib')
    company_list = soup.find_all(href=re.compile('/jyzx/newSystem/noticeDetail.jsp?'))
    date_list = soup.select('.date')
    for i in range(len(company_list)):
        try:
            date = date_list[i].text.strip()[:10]
            company_name = company_list[i].text.strip()
            if pattern.match(date):
                print(date, company_name)
                redis.save_info(table_name, date, company_name)
                print("=====")
        except BaseException as e:
            util.format_err(e)
            pass

if __name__ == '__main__':
    get_scut_recuit()

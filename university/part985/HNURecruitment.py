import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util
import re

# 因海南大学与湖南大学简称相同，所以用大写的表示湖南大学
table_name = "HNU_company_info"  # 湖南大学


def get_hnu_recuit():
    print("开始获取湖南大学数据=====================")
    url = "http://scc.hnu.edu.cn/newsjob!getMore.action?"
    host = "scc.hnu.edu.cn"
    headers = util.get_header(host=host)
    redis = jedis.jedis()
    redis.clear_list(table_name)
    for i in range(1, 310):  # 一共310页，102页及其以前都是2017年的
        try:
            params = {'p.currentPage': '%d' % i, 'Lb': '1'}
            html = requests.get(url=url, headers=headers, params=params).text
            parse_info(html, redis)
        except BaseException as e:  # 还不太会错误处理机制
            util.format_err(e)
            break
        finally:
            print('获取湖南大学第 %d 页(共310页)数据完成' % i)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def parse_info(html, redis):
    bf = BeautifulSoup(html, 'lxml')
    bf1 = bf.find_all('div', class_='r_list1')
    bf2 = BeautifulSoup(str(bf1), 'lxml')
    date_list = bf2.find_all('span')
    company_list = bf2.find_all(href=re.compile('articledetail\?t.PostId='))
    for i in range(len(date_list)):
        try:
            date = date_list[i].text.replace('/', '-')
            company_name = company_list[i].text.strip()
            if company_name.find('取消') == -1 and date != '':
                redis.save_info(table_name, date, company_name)
        except BaseException as e:
            util.format_err(e)
            continue


if __name__ == '__main__':
    get_hnu_recuit()

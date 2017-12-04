# 不同的beautifulsoup 方法
# @author 刘航
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util
import re


table_name = "sxu_company_info"    # 山西大学


def get_sxu_recuit():
    print("开始获取山西大学数据=====================")
    url = "http://job.sxu.edu.cn/News_More.asp?"
    host = "job.sxu.edu.cn"
    headers = util.get_header(host=host)
    redis = jedis.jedis()                 # 实例化一个类，用于存储格式化数据的类   1
    redis.clear_list(table_name)
    for i in range(1, 323):  # 一共322页
        try:
            params = {'NewsTypeId': '4', 'page': '%d' % i}
            html = requests.get(url=url, headers=headers, params=params).content.decode('gb2312')
            parse_info(html, redis)
        except BaseException as e:  # 还不太会错误处理机制
            util.format_err(e)
            break
        finally:
            print('获取山西大学第 %d 页(共322页)数据完成' % i)
    redis.add_university(table_name)           # 添加学校到github中      2
    redis.add_to_file(table_name)              # 添加表到文件中           3


def parse_info(html, redis):
    bf = BeautifulSoup(html, 'lxml')
    bf1 = bf.find_all('table',class_='ntblbk')
    bf2 = BeautifulSoup(str(bf1), 'lxml')
    date_list = bf2.find_all(align='right', class_=re.compile('td_line_col'))
    company_list = bf2.find_all(href=re.compile('News_View.asp\?NewsId='))
    for i in range(len(date_list)):
        try:
            date = date_list[i].text.strip()[1:-1]
            company_name = company_list[i].text.strip()
            redis.save_info(table_name, date, company_name)    # 只管用这个来保存，保存每一个公司及日期       4
        except BaseException as e:
            util.format_err(e)
            continue


if __name__ == '__main__':
    get_sxu_recuit()

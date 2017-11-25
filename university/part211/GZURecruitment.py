import re
import requests

from jedis import jedis
from util import util
from bs4 import BeautifulSoup

pattern = re.compile('共 [0-9]+ 页')
pattern2 = re.compile('第[0-9]+期')
pattern3 = re.compile('[0-9]+第期')
# 贵州大学
table_name = 'gzu_company_info'
def get_gzu_recruit():
    base_url = 'http://jobs.gzu.edu.cn/gzujobs/client/recruitment/meet?page='
    req = requests.Session()
    host = 'jobs.gzu.edu.cn'
    content = req.get(url=base_url + str(1), headers=util.get_header(host)).content.decode('utf-8')
    page_num = get_page_num(content)
    redis = jedis.jedis()
    redis.clear_list(table_name)
    for i in range(1, page_num + 1):
        url = base_url + str(i)
        print(url)
        content = req.get(url=url, headers=util.get_header(host)).content.decode('utf-8')
        parse_info(content, redis, i)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def get_page_num(content):
    soup = BeautifulSoup(content, 'html5lib')
    page_num = re.findall(pattern, str(soup))[0][1:-1].strip()
    return int(page_num)


def parse_info(content, redis, page):
    soup = BeautifulSoup(content, 'html5lib')
    company_list = soup.find_all(href=re.compile('/gzujobs/client/jobsinfor/'))
    date_list = soup.select('.time')
    for i in range(0, len(company_list)):
        company_name = company_list[i].text.strip()
        if page < 128:
            try:
                year = re.findall(pattern2, company_name)[0][1:-1]
                if int(year) > 624:
                    year = '17'
                else:
                    year = '16'
            except IndexError:
                try:
                    year = re.findall(pattern3, company_name)[0][1:-1]
                except BaseException as e:
                    util.format_err(e)
                    continue
        else:
            try:
                year = re.findall(re.compile('[0-9]+-?-?第[0-9]+期'), company_name)[0][0:2]
            except IndexError:
                try:
                    year = re.findall(re.compile('[0-9]+-?－?[0-9]+期'), company_name)[0][0:2]
                except BaseException:
                    util.format_err(e)
                    continue
            if year == '44':
                year = '09'
        date = '20' + str(year) + '-' + date_list[i].text[1:-1]

        company_name = company_name.split('(')[0].strip()
        print(company_name, date)
        redis.save_info(table_name, date, company_name)

if __name__ == '__main__':
    get_gzu_recruit()

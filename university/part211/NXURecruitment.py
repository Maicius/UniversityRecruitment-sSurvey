# coding = utf-8
import re
import requests
from bs4 import BeautifulSoup

from jedis import jedis
from util import util

table_name = 'nxu_company_info'
date_pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')


# 宁夏大学
def get_nxu_recruit():
    url = 'http://www.nxujob.com/news/news-list.php?id=27&page='
    req = requests.Session()
    headers = util.get_header('www.nxujob.com')
    redis = jedis.jedis()
    redis.clear_list(table_name)
    for i in range(1, 48):
        print(url + str(i))
        content = req.get(url=url + str(i), headers=headers).content.decode('gbk')
        soup = BeautifulSoup(content, 'html5lib')
        url_list = soup.find_all(href=re.compile('http://www.nxujob.com/news/news-show.php'), attrs={'target': '_blank'})
        for j in range(10):
            detail_url = url_list[j].attrs['href']
            print(detail_url)
            detail = req.get(url=detail_url, headers=headers).content.decode('gbk')
            parse_info(detail, redis)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


def parse_info(content, redis):
    soup = BeautifulSoup(content, 'html5lib')
    company_name = re.findall(re.compile('<h1>.*?</h1>'), str(soup))[0][4:-5].strip()
    date = re.findall(date_pattern, str(soup))[0]
    if company_name == '宁夏大学2018届毕业生校园秋季“双选”洽谈会部分企业名单':
        com_name_list = soup.find_all(attrs={'height': '19', 'width': '320'})
        for i in range(1, len(com_name_list)):
            com_name = com_name_list[i].text.strip()
            redis.save_info(table_name, date, com_name)
    print(company_name, date)
    if company_name.find('邀请函') == -1:
        redis.save_info(table_name, date, company_name)

if __name__ == '__main__':
    get_nxu_recruit()

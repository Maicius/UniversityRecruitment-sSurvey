import re
import requests
from jedis import jedis
from util import util
from bs4 import BeautifulSoup

# 中国海洋大学
pattern = re.compile('<a class="a1">[0-9]+')
table_name = "ouc_company_info"


def get_ouc_recruit():
    print("开始获取中国海洋大学数据=====================")
    url = "http://career.ouc.edu.cn/html/zp_info/campus/index.html"
    host = 'career.ouc.edu.cn'
    headers = util.get_header(host)
    req = requests.Session()
    res = req.get(url=url, headers=headers).content.decode('gbk')
    redis = jedis.jedis()
    redis.clear_list(table_name)
    soup = BeautifulSoup(res, 'html5lib')
    total_infos = int(re.findall(pattern, str(soup))[0][14:])
    page_num = total_infos // 20 + 1
    for i in range(1, page_num + 1):
        try:
            if i == 1:
                url = "http://career.ouc.edu.cn/html/zp_info/campus/index.html"
            else:
                url = "http://career.ouc.edu.cn/html/zp_info/campus/" + str(i) + ".html"
            content = req.get(url=url, headers=headers).content.decode('gbk')
            parse_info(content, redis)
        except BaseException as e:
            util.format_err(e)
    redis.add_university(table_name)
    redis.add_to_file(table_name)
    print("获取中国海洋大学数据完成=====================")


def parse_info(content, redis):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all(href=re.compile('http://career.ouc.edu.cn/html/zp_info/campus/'))
    date_list = soup.select('.xiaozhao_list_time')
    for i in range(2, 21):
        company_name = company_list[i].text.strip()
        date = date_list[i - 2].text.strip()[:10]
        redis.save_info(table_name, date, company_name)
        print(company_name, date)


if __name__ == '__main__':
    get_ouc_recruit()

import requests
from bs4 import BeautifulSoup
import re
from jedis import jedis
from util import util


# 华北电力大学
# 包括宣讲会与双选会
def get_ncepu_recruit():
    table_name = "ncepu_company_info"
    base_url = "http://job.ncepu.edu.cn/teachin/index?domain=ncepu&page="
    req = requests.Session()
    redis = jedis.jedis()
    redis.clear_list(table_name)
    host = "job.ncepu.edu.cn"
    header = util.get_header(host)
    # 获取宣讲会信息
    for i in range(1, 34):
        res = req.get(headers=header, url=base_url + str(i))
        html = res.content.decode("utf-8")
        parse_info(html, redis, table_name)
    get_double_choose(req, header, re)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def get_double_choose(req, header, redis):
    url = "http://job.ncepu.edu.cn/jobfair/index?domain=ncepu"
    content = req.get(url=url, headers=header).content
    html = content.decode("utf-8")
    soup = BeautifulSoup(html, "html5lib")
    com_list = soup.find_all(href=re.compile('/jobfair/view/id'))
    for item in com_list:
        detail_url = item.get('href')
        print(detail_url)
        detail_url = "http://job.ncepu.edu.cn" + detail_url
        detail = req.get(url=detail_url, headers=header).content.decode("utf-8")
        detail_soup = BeautifulSoup(detail, "html5lib")
        detail_text = detail_soup.text
        # 由于格式十分不固定，所以使用正则表达式来提取内容
        companys = detail_text.find("详情")
        print(companys)

    print(com_list)


def parse_info(html, redis, table_name):
    soup = BeautifulSoup(html, "html5lib")
    company_list = soup.find_all(href=re.compile('/teachin/view/id/'))
    dateList = re.findall(re.compile('([0-9]{4}-[0-9]{2}-[0-9]{2})|(活动已取消)'), str(soup))
    print(company_list)
    try:
        for j in range(len(company_list)):
            company_name = company_list[j].text.strip()
            date = dateList[j][0]
            if date != '':
                print(company_name)
                print(date)
                redis.save_info(table_name, date, company_name)
    except IndexError:
        print("finish")
    except ConnectionError as e:
        redis.handle_error(e, table_name)


if __name__ == '__main__':
    get_ncepu_recruit()

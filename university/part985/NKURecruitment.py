# coding = utf-8

import json
import re
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util

table_name = "nku_company_info"
pattern = re.compile('margin-bottom:0px;">时间')


# 南开大学
def get_nku_recruit():
    # 宣讲会
    url = 'http://career.nankai.edu.cn/Home/Reccalender/doxuanjiang'
    # 双选会
    url2 = 'http://career.nankai.edu.cn/Home/Reccalender/doshuangxuan'
    host = 'career.nankai.edu.cn'
    header = util.get_header(host)
    header['referer'] = 'http://career.nankai.edu.cn/reccalender/index.html'
    header[
        'cookie'] = 'yunsuo_session_verify=5374b1e89d110421560f5e8e3182d03c; PHPSESSID=632an0himtafj6me8379r8fkn4; Hm_lvt_6eb8a37eb57545b46494b26e6136af4a=1511532968; Hm_lpvt_6eb8a37eb57545b46494b26e6136af4a=1511533002'
    years = ['2016, 2017']
    req = requests.Session()
    redis = jedis.jedis()
    for year in years:
        company_list = req.post(url=url, headers=header, data={'year': year}).content.decode('unicode-escape')
        parse_info(redis, company_list)

    # 获取双选会
    recruit_list = req.post(url=url2, headers=header, data={'year': 2017}).content.decode('unicode-escape')
    recruit_list = json.loads(recruit_list)
    for item in recruit_list:
        id = item['id']
        date = item['starttime']
        title = item['title']
        print("===============================")
        print(title, id)
        recruit_url = 'http://career.nankai.edu.cn/Home/Recruitment/content/type/1/id/' + str(id) + '.html'
        content = req.get(url=recruit_url, headers=header).content.decode("utf-8")
        parse_recruit_info(redis, content, date, id)
    redis.add_university(table_name)
    redis.add_to_file(table_name)


def parse_recruit_info(redis, content, date, id):
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all(href=re.compile("/recruitment/company"))
    print(date)
    for item in company_list:
        company_name = item.text.strip()
        # print(company_name)
        redis.save_info(table_name, date, company_name)
    print("获取双选会完成")

    # 2018大型双选会
    if int(id) == 62:
        company_list = soup.find_all(attrs={'style': 'font-size:14px;font-family:\'微软雅黑\',sans-serif;color:#666666'})
        for i in range(13, 211, 2):
            try:
                company_name = company_list[i + 1].text.strip()
                # print(company_name)
                redis.save_info(table_name, date, company_name)
            except BaseException as e:
                util.format_err(e)
                break

    # 大型双选会
    if int(id) == 69:
        company_list = soup.find_all(attrs={'style': 'font-size:14px;font-family:\'微软雅黑\',sans-serif;color:#666666'})
        for i in range(14, 179, 2):
            try:
                company_name = company_list[i + 1].text.strip()
                # print(company_name)
                redis.save_info(table_name, date, company_name)
            except BaseException as e:
                util.format_err(e)
                break

    # 国有企业双选会
    if int(id) == 68:
        company_list = soup.find_all(attrs={'style': 'font-size: 19px'})
        for i in range(0, len(company_list) - 1):
            company_name = company_list[i + 1].text
            # print(company_list[i])
            # print(company_name)
            redis.save_info(table_name, date, company_name)

    if len(company_list) == 0:
        print("failed")


def parse_info(redis, content):
    company_list = json.loads(content)
    for data in company_list:
        date = data['retime']
        company_name = data['title']
        print(company_name)
        redis.save_info(table_name, date, company_name)


if __name__ == '__main__':
    get_nku_recruit()

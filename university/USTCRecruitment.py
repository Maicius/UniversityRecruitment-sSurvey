import json

import requests
from Util import Util


# 中国科学技术大学就业信息
def get_ustc_recruit():
    # 专场招聘会URL
    base_url = "http://www.job.ustc.edu.cn/API/Web/Recruit.ashx?rand=0.10286254897924929&pagesize=20&action=list&keyword=&pageindex="
    req = requests.Session()
    host = "www.job.ustc.edu.cn"
    table_name = "ustc_company_info"
    header = Util.get_header(host)
    re = Util.jedis()
    re.connect_redis()
    for i in range(1, 25):
        url = base_url + str(i)
        res = req.get(headers=header, url=url)
        content = res.content.decode("utf-8")
        parse_info(content, re, table_name)
    get_communicate(req, re, header, table_name)
    re.add_university(table_name)
    re.add_to_file(table_name)
    print("finish")


# 就业供需洽谈会
def get_communicate(req, re, header, table_name):
    print("开始获取双选会")
    com_url = "http://www.job.ustc.edu.cn/API/Web/Recruit.ashx"
    list_url = "http://www.job.ustc.edu.cn/API/Web/Recruit.ashx"
    list_params = {'pagesize': 100, 'pageindex': 1, 'action': 'recruitlist', 'rand': 0.6186712935744574}
    params = {'pagesize': 100, 'pageindex': 1, 'action': 'recruitcompany', "rid": 1010, 'rand': 0.6186712935744574}
    res = req.post(url=list_url, headers=header, data=list_params)
    content = res.content.decode("utf-8")
    # print(content)
    content = json.loads(content)
    page_count = content['PageCount']
    for i in range(1, page_count + 1):
        for item in content['data']:
            date = item['HoldBegin'][0:10]
            id = item['ID']
            print(date, id)
            params['rid'] = id
            content = req.post(headers=header, url=com_url, data=params).content.decode("utf-8")
            content = json.loads(content)
            page_count2 = content['PageCount']
            # 就业供需洽谈会可能有多页，是100一页
            for j in range(1, page_count2 + 1):
                params['pageindex'] = j
                data = req.post(headers=header, url=com_url, data=params).content.decode("utf-8")
                parse_com_data(data, re, date, table_name)
                print("page:" + str(j) + "finish")


def parse_com_data(content, re, date, table_name):
    print(content)
    content = json.loads(content)
    for item in content['CompanyList']:
        company_name = item['CompanyName']
            # print(company_name)
        re.save_info(table_name, date, company_name)


def parse_info(content, re, table_name):
    content = json.loads(content)
    for item in content['data']:
        company_name = item['Theme']
        date = item['HoldDate'][0:10]
        print(date)
        print(company_name)
        re.save_info(table_name, date, company_name)


if __name__ == "__main__":
    get_ustc_recruit()

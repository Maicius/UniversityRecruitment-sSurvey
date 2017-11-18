# coding = utf-8
import datetime
import json

from jedis import jedis
from util import util
import requests
from bs4 import BeautifulSoup
table_name = "pku_company_info"


# 获取北京大学的宣讲会信息
def get_pku_recruit():
    print("PKU Begin ===================================================")
    base_url = "https://scc.pku.edu.cn/information/base-job-fair!findFairInfoByMonth.action"
    host = "scc.pku.edu.cn"
    headers = util.get_header(host)
    headers['Referer'] = "https://scc.pku.edu.cn/timeline?fairDate=2017-11-03%2000:00"
    headers[
        'cookie'] = "Hm_lvt_f77188aadf0698598108fbf1f0e5df52=1509938240,1510453941; JSESSIONID=A07EA9A7A0B89A27E64ABB70E7D2C5FD; Hm_lpvt_f77188aadf0698598108fbf1f0e5df52=1510454286"
    req = requests.Session()
    re = jedis.jedis()
    re.connect_redis()
    re.clear_list(table_name)
    #
    # 获取宣讲会信息
    for i in range(1, 13):
        month = i
        yearMonth = datetime.date(2017, month, i)
        yearMonth = util.get_month(yearMonth)
        data = {'yearMonth': yearMonth}
        # data = {'yearMonth': '2017-01'}
        # req.get(url="https://scc.pku.edu.cn", verify=False)
        res = req.post(headers=headers, url=base_url, data=data, verify=False)
        content = res.content.decode("utf-8")
        parse_info(content, re)

    # 获取双选会信息
    url = "https://scc.pku.edu.cn/home!bigFairJobInfo.action"
    url2 = "https://scc.pku.edu.cn/home!bigFairJobInfo.action"
    data2 = {'start': 0, 'limit': 600, 'currentPage': 1}
    headers['Referer'] = "https://scc.pku.edu.cn/home!speciaPreach.action"
    headers[
        'cookie'] = "Hm_lvt_f77188aadf0698598108fbf1f0e5df52=1509938240,1510453941,1510459302; JSESSIONID=A941D7C64B752EDE61AAD5093876A35E; Hm_lpvt_f77188aadf0698598108fbf1f0e5df52=1510460247"
    headers['X-Requested-With'] = "X-Requested-WithXMLHttpRequest"
    headers['Cache-Control'] = "no-cache"
    req.get(url=url, headers=headers, verify=False)
    headers['Referer'] = "https://scc.pku.edu.cn/home!bigFairJobInfo.action"
    info = req.post(headers=headers, url=url2, data=data2, verify=False)
    print("get info success")
    parse_info2(info.content.decode("utf-8"), re)
    re.add_university(table_name)
    re.add_to_file(table_name)
    print("PKU Finish ===================================================")


# 解析双选会的数据
# def parse_info2(content, re):
#     info = json.loads(content)
#     for item in info['data']:
#         company_name = item['enterpriseName']
#         if item['create_time'].find('2017') != -1:
#             date = "2017-12-03"
#         elif item['create_time'].find('2016') != -1:
#             date = "2016-12-04"
#         else:
#             date = "2015-12-12"
#         re.save_info(table_name, date, company_name)
def parse_info2(content, re):
    info = BeautifulSoup(content, "html5lib")
    print(info)
    table_list = info.table.find_all("td")
    length = len(table_list)

    for i in range(0, length - 3, 3):
        print(i)
        try:
            company_name = table_list[i + 1].text.strip()
            # 去掉实习
            if company_name.find("实习") == -1:
                if company_name.find("]") != -1:
                    company_name = company_name.split("]")[1]
                date = table_list[i + 2].text.strip()
                print(company_name + ":" + date)
                re.save_info(table_name, date, company_name)
        except BaseException as e:
            print(len(table_list))
            print(e)
            continue
    # print(table_list)


# 解析宣讲会的数据
def parse_info(content, re):
    content = json.loads(content)
    for item in content:
        # 忽略掉已取消的宣讲会
        if item['offline'] == 0:
            # 存储宣讲会日期的字段在fairDate或startTime
            if 'fairDate' in item:
                date = item['fairDate'][0:10]
            else:
                date = item['startTime']
            company_name = item['title']
            print(date + ":" + company_name)
            re.save_info(table_name, date, company_name)
        else:
            continue


if __name__ == '__main__':
    get_pku_recruit()

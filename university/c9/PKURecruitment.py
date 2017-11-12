# coding = utf-8
import datetime
import json

from jedis import jedis
from util import util
import requests

table_name = "pku_company_info_test"

# 获取北京大学的宣讲会信息
def get_pku_recruit():

    base_url = "https://scc.pku.edu.cn/information/base-job-fair!findFairInfoByMonth.action"
    host = "scc.pku.edu.cn"
    headers = util.get_header(host)
    headers['referer'] = "https://scc.pku.edu.cn/timeline?fairDate=2017-11-03%2000:00"
    headers['cookie'] = "Hm_lvt_f77188aadf0698598108fbf1f0e5df52=1509938240,1510453941; JSESSIONID=A07EA9A7A0B89A27E64ABB70E7D2C5FD; Hm_lpvt_f77188aadf0698598108fbf1f0e5df52=1510454286"
    req = requests.Session()
    re = jedis.jedis()
    re.connect_redis()

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
    re.add_university(table_name)
    re.add_to_file(table_name)


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

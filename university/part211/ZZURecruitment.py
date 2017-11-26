# 郑州大学
import json

import requests

from jedis import jedis
from util import util

table_name = "zzu_company_info"


# 郑州大学
def get_zzu_recruit():
    url = "http://job.zzu.edu.cn:9009/service/business/college/jobfair/jobFairInfo/getCalendarInfo.xf"

    req = requests.Session()
    host = 'job.zzu.edu.cn:9009'
    headers = util.get_header(host)
    headers['referer'] = 'http://job.zzu.edu.cn/p/page/jobCalendar.html?channel_code=XJH&type=0'
    redis = jedis.jedis()
    redis.clear_list(table_name)
    year = 2018
    # 从 2017年一直退回到2012年
    for i in range(72, 0, -1):
        month = i % 12
        if month == 0:
            year = year - 1
            month = 12
        params = {
            'remark': '0',
            'year': str(year),
            'month': str(month)
        }
        print(params)
        res = req.post(url=url, headers=headers, data=params)
        content = res.content.decode('utf-8')
        parse_info(content, redis)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


def parse_info(content, redis):
    content = json.loads(content)
    trList = content['result']['trList']
    print(trList)
    for item in trList:
        for day in item['tdList']:
            if day is not None:
                if 'careerList' in day:
                    careerList = day['careerList']
                    if careerList is not None:
                        try:
                            for data in careerList:
                                date = data['mergeStartTime']
                                company = data['mergeTitle']
                                print(date, company)
                                redis.save_info(table_name, date, company)
                        except BaseException as e:
                            util.format_err(e)
                            pass

if __name__ == '__main__':
    get_zzu_recruit()

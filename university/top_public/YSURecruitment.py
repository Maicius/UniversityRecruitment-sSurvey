import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep
from json import loads
import datetime


def get_one_page_data(date, redis, table_name):
    url = 'http://job.ysu.edu.cn/zftal-web/zfjy!wzxx/xjhxx_cxWzXjhxxByRlAjax.html'
    form_data = {
        'xjhrq': date.strftime('%Y-%m-%d'),
    }
    response = requests.post(url, form_data)
    json_data = loads(response.text)
    if json_data:
        for i in json_data:
            company_name = i['xjhmc']
            print(company_name)
            date = i['xjhrq']
            redis.save_dict(table_name, dict(
                company_name=company_name,
                date=date,
            ))
    else:
        print('nothing')


def get_ysu_recruitment():
    # 燕山大学
    table_name = 'ysu_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    # 2014-4-1 到 当前日期
    begin_date = datetime.date(2014, 4, 1)
    current_date = datetime.date.today()
    try:
        while begin_date != current_date:
            get_one_page_data(begin_date, redis, table_name)
            print(str(begin_date) + ' done!')
            begin_date += datetime.timedelta(days=1)
    except BaseException as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_ysu_recruitment()

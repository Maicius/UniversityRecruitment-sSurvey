import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_week_data(week, redis, table_name):
    url = 'http://jy.ncut.edu.cn/front/channel.jspa?channelId=766&weekOfMonth=1&curWeek=' + str(
        week) + '&property=0'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    table_node = soup.find('table')

    # 过滤空项
    trs = [x for x in table_node.find_all('tr') if x.find('a') is not None]

    # 奇数行公司名, 偶数行日期
    company_name_trs = trs[0::2]
    date_trs = trs[1::2]

    companies_name = []
    dates = []
    for item in company_name_trs:
        companies_name.append(item.find('a').find('font').text)
    for item in date_trs:
        date = item.find('a').find('font').text[0:6]
        date = date.replace('月', '-').strip()
        # -100 -- -52 2015年
        # -51  -- 0 2016年
        # 1    -- .... 2017年
        if -100 <= week <= -52:
            date = '2015-' + date
        if -51 <= week <= 0:
            date = '2016-' + date
        if 1 <= week:
            date = '2017-' + date
        dates.append(date)
    for i in range(len(companies_name)):
        company_name = companies_name[i]
        date = dates[i]
        # print(company_name)
        # print(date)
        redis.save_dict(table_name, dict(
            company_name=company_name,
            date=date,
        ))


def get_ncut_recuitment():
    # 北方工业大学
    table_name = 'ncut_company_info'

    redis = jedis.jedis()
    redis.connect_redis()
    redis.clear_list(table_name)

    # -100周 到 60周
    begin_week = -100
    end_week = 60
    try:
        for i in range(begin_week, end_week):
            get_one_week_data(i, redis, table_name)
            print('week ' + str(i) + ' done!')
    except TimeoutError as e:
        print('test')
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_ncut_recuitment()

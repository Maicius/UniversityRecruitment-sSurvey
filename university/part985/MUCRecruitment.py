import requests
from bs4 import BeautifulSoup
from jedis import jedis
from time import sleep


def get_one_week_data(week, redis, table_name, s):
    url = 'http://www.career.muc.edu.cn/front/channel.jspa?channelId=766&weekOfMonth=1&curWeek=' + str(
        week) + '&property='
    response = s.get(url=url)
    soup = BeautifulSoup(response.text, 'html5lib')
    table_node = soup.find('tbody', attrs={'class': 'xjzph'})
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
        # 0 ->... 2017年
        if 0 <= week:
            date = '2017-' + date
        dates.append(date)
    for i in range(len(companies_name)):
        redis.save_dict(table_name, dict(
            company_name=companies_name[i],
            date=dates[i]
        ))


def get_muc_recuitment():
    # 中央民族大学
    table_name = 'muc_company_info'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    session.headers.update(header)
    # 0周 到 55周
    begin_week = 0
    end_week = 51
    try:
        for i in range(begin_week, end_week):
            get_one_week_data(i, redis, table_name, session)
            print('week ' + str(i) + ' done!')
    except TimeoutError as e:
        print('test')
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_muc_recuitment()

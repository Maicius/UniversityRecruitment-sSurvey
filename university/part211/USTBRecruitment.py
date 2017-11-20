import requests
from bs4 import BeautifulSoup


def get_one_week_date(week, redis, table_name):
    url = 'http://job.ustb.edu.cn/front/channel.jspa?channelId=763&parentId=763&weekOfMonth=1&curWeek=' + str(
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
        companies_name.extend(item.find('a').find('font').text)
    for item in date_trs:
        date = item.find('a').find('font').text[0:6]
        date = date.replace('月', '-')
        # -121 -- -106 2014年
        # -105 -- -53 2015年
        # -54  -- -1 2016年
        # 0 ->... 2017年
        if -121 <= week <= -106:
            date = '2014-' + date
        if -105 <= week <= -53:
            date = '2014-' + date
        if -54 <= week <= -1:
            date = '2014-' + date
        if 0 <= week:
            date = '2014-' + date
        dates.extend(date)
    for i in range(len(companies_name)):
        print(companies_name[i] + dates[i])


if __name__ == '__main__':
    get_one_week_date()

import requests
from bs4 import BeautifulSoup
from jedis import jedis

# 成都信息工程大学
def get_data(table_name, redis):
    host = 'http://cuit.njc100.com/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=yjb'
    url = 'http://cuit.njc100.com/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&'

    form_data = {
        'pageMethod': 'pager',
        'resetPageSize': '400',
        'pageNum': '1',
    }
    s = requests.session()
    # 获取cookie
    s.get(host)

    response = s.post(url, data=form_data)
    soup = BeautifulSoup(response.text, 'html5lib')
    form_node = soup.find('div', attrs={'class': 'z_newsl'})
    lists = form_node.find_all('li')[1:]
    for i in lists:
        divs = i.find_all('div')
        company_name = divs[2].contents[0].text
        date = divs[0].text
        print(company_name + date)
        redis.save_dict(table_name, dict(
            date=date,
            company_name=company_name,
        ))


def get_cuit_recruit():
    # 成都信息工程大学
    print("成都信息工程大学开始================================")
    table_name = 'cuit_company_info'
    try:
        redis = jedis.jedis()
        redis.clear_list(table_name)
        get_data(table_name, redis)
        redis.add_to_file(table_name)
        redis.add_university(table_name)
    except BaseException as e:
        print("成都信息工程大学:")
        print(e)
        pass
    print("成都信息工程大学开始================================")


if __name__ == '__main__':
    get_cuit_recruit()

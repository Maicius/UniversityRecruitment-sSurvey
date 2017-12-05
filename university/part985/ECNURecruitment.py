import requests
import re
from bs4 import BeautifulSoup
from jedis import jedis

__VIEWSTATE_pattern = re.compile('__VIEWSTATE\|(.*?)\|')
__EVENTVALIDATION_pattern = re.compile('__EVENTVALIDATION\|(.*?)\|')


def get_session():
    s = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',

    }
    s.headers.update(header)
    return s


def get_content(s, url, __EVENTVALIDATION, __VIEWSTATE):
    form_data = {
        'ctl00$cphIMmain$ScriptManagerListMessage': 'ctl00$cphIMmain$ctl00$OrangeTabcontent_62|ctl00$cphIMmain$ctl00$btnPN2',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': 'CEE9BCEF',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': __EVENTVALIDATION,
        '__ASYNCPOST': 'true',
        'ctl00$cphIMmain$ctl00$btnPN2': '',
    }
    response = s.post(url, data=form_data)
    return response.text


def parse_content(content, redis, table_name):
    soup = BeautifulSoup(content, 'html5lib')
    node = soup.find('table', attrs={'id': 'gvMEL2List'})
    if node:
        trs = node.find_all('tr')[1:]
        for tr in trs:
            tds = tr.contents
            company_name = tds[1].find('a').text.strip()
            date = tds[2].text.strip()[:10]
            print(date)
            redis.save_dict(table_name, dict(
                company_name=company_name,
                data=date,
            ))
        # 返回结束标志
        return date == '2011-12-01'
    else:
        pass


# 利用当前页面的隐含参数作表单参数访问下一页
def parse_parameters(content):
    __EVENTVALIDATION = __EVENTVALIDATION_pattern.findall(content)[0]
    __VIEWSTATE = __VIEWSTATE_pattern.findall(content)[0]
    return __EVENTVALIDATION, __VIEWSTATE


def get_ecnu_recruitment():
    # 华东师范大学
    table_name = 'ecnu_company_info'
    url = 'http://www.career.ecnu.edu.cn/commonpage/ListMessage.aspx?infotype=el'

    redis = jedis.jedis()
    redis.clear_list(table_name)

    # 初始参数
    __VIEWSTATE = 'S+WPBHsLsy12D8przcyE7qpkPYu9cdeAgBUifZLLgj2ut3Fs4gXEqRxDo53bG5pn6gpuyVbz6z4e/ERztf5uEEU/rSTn6GdPhUhZ0yRuyTW45lZpMU2xF2qfExaOT6AmTSx1dHGOPHWYofJSK62Vur+uIMgf4En6eCrhhmsyX72Hsy19sQPEeWC5Qaea6FddgJrFo+GjkukltQrrQho2iDFFYK2HPvceAqdmHVpL1gS16SWRF+oZabG7ptN0brscjEVCS/5sEHvNUrMLwg/9b+osSqda1jJJJTVidnu0yjAAD/JlSZx60O6i5zmHdlgDIHDVyD/oqndryIRowYuo1oRd3cQ0f2qr9yeipbvDXBLRpXA6Z0qPCo6/JoRj6vYQGwLHwqA7SPovunrwM3tO1ZQxeMajIUENxhqzNOSFXNGO60GAFaIunfhe/b7F5sAGBIniqIX2W+U66Np7nAmoqEzaTGZHjadMnEDDheTAg1yXcFZxWKCXtjT5i3aQ6FdMtwpi3U7nX2qHnxBsmMaKqkm86liXgR1WwnUlzf8t8YvT/O/j88lnbcZomMNR1xxpGL3LIkD6XxiyiLtSB9iPY/uKs1mcRWUJxYfbNAHMn7hqTsfBvACUqOP72LTf9QYtgRDPyXv5jp4kIMuV9VhhG/kzggveXUFK1UZ0Oy6tQamYS52lBMp/6F8ibpwAmNEf'
    __EVENTVALIDATION = 'PzbwP/Zoy+Gxtp8jeRMHlsqDlG8FHGyiIB0rnsPeHlR5GCKT3S/ijcmOCnvo+xG7JwLukL/LacFOXZFw/Ksx+KUsoZ5uBc6y8n05Seo7Wade+Y1hYQWQa9JCP2Ftf596eTYB4Q7kpKSm44YMgva6YoHVJtDHgW0rEB2az5xE5eqNtr2nqNUAkubtOxNWgSwSbPHlDtx84OZ27rw2cwClP+qtthyJx2oeH1S/SfIguB74I1who3k+Hc18vSj1+QGOHdP44gI6o3KDbDh4ZkAsT7+lj0uAZGq7ICg9UIgKWkprRoQKnd0QdrpexSij4KvJP3rQ0a8Q1ZV0K4/Fi5tAAXWtL/n0oQOwoxUbD0PUbTBZLY1FrcLH0Gdm6SsS45G9'

    session = get_session()

    page_count = 1
    # 结束条件为 只有一条信息
    try:
        while True:
            content = get_content(session, url, __EVENTVALIDATION, __VIEWSTATE)
            __EVENTVALIDATION, __VIEWSTATE = parse_parameters(content)
            end = parse_content(content, redis, table_name)
            print('parse %d page !' % page_count)
            page_count += 1
            if end:
                print('end!')
                break
    except BaseException as e:
        redis.handle_error(e, table_name)
    redis.add_to_file(table_name)
    redis.add_university(table_name)


if __name__ == '__main__':
    get_ecnu_recruitment()

# 获取上海交通大学就业信息
import re
import requests
from bs4 import BeautifulSoup

from jedis import jedis
from util import util
pattern = re.compile('[0-9]+-[0-9][0-9]-[0-9][0-9]')
redis = jedis.jedis()
redis.clear_list("sjtu_company_info_2018")

def get_sjtu_rescruit():
    host = "www.job.sjtu.edu.cn"
    first_url = "http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=yjb"
    base_url = "http://www.job.sjtu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
    header = util.get_header(host)

    req = requests.Session()
    res = req.get(headers=header, url=first_url).content.decode("utf-8")
    table_name = "sjtu_company_info"
    page_num = 39
    page_num = get_page_num(content=res)
    # 解析数据
    get_rescruit(base_url, req, header, table_name, page_num, 14, 64, 1)
    # 在大学列表里新增表名
    redis.add_university(table_name)

    # 保存到json文件
    redis.add_to_file(table_name)


def get_rescruit(base_url, req, header, table_name, page_num, index_begin, index_end, company_index):
    for i in range(0, page_num):
        url = base_url + str(i)
        #
        # print(url)
        res = req.get(headers=header, url=url)
        content = res.content.decode("utf-8")
        parse_info(content, table_name, index_begin, index_end, company_index)


def parse_info(content, table_name, index_begin, index_end, company_index):
    soup = BeautifulSoup(content, "html5lib")
    company_info = soup.find_all('li')
    for num in range(index_begin, index_end):
        try:
            # print(company_info[num].text)
            company = company_info[num].text
            # company_name = company[2]
            # company_date = company[4]
            infos = company.split("\n\t")
            date = infos[4].strip()
            company_name = infos[company_index].strip()
            # print(company)
            # 在存储之前匹配一下日期格式是否正确，避免在最后一页时存储垃圾数据
            if pattern.match(date):
                redis.save_info(table_name, date, company_name)
        except IndexError:
            print(len(company_info))
            continue
        except ConnectionError as e:
            redis.print_redis_error(e)
            continue
        except BaseException as e:
            redis.handle_error(e, table_name)


# 获取总页数
def get_page_num(content):
    num = re.findall('(/&nbsp;[1-9]+&nbsp;页)', content)

    try:
        num = re.findall('[1-9]+', num[0])
        page_num = int(num[0])
        print(page_num)
        return page_num
    except BaseException as e:
        print("Failed to find total page num =================================")
        print(e)
        print("=================================")
        return 265

if __name__ == '__main__':
    get_sjtu_rescruit()
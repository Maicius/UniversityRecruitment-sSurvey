# coding = utf-8
import traceback

import requests
from bs4 import BeautifulSoup
from Util import Util


# 上海交通大学与四川大学的就业网是一个模板
class Recruitment(object):

    def __init__(self):
        self.re = Util.jedis()
        self.re.connect_redis()

    # 获取四川大学宣讲会信息
    def get_scu_recruit(self):
        host = 'jy.scu.edu.cn'
        first_url = "http://jy.scu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx"
        base_url = "http://jy.scu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
        req = requests.Session()
        scu_header = Util.get_header(host)
        res = req.get(headers=scu_header, url=first_url)
        content = res.content.decode("utf-8")
        table_name = "scu_company_info_test"
        page_num = 224
        index_begin = 8
        index_end = 28
        self.parse_info(content, table_name, index_begin, index_end, 2)
        self.get_rescruit(base_url, req, scu_header, table_name, page_num, index_begin, index_end, 2)
        self.re.add_university(table_name)
        self.re.add_to_file(table_name)

    # 获取上海交通大学就业信息
    def get_sjtu_rescruit(self):
        host = "www.job.sjtu.edu.cn"
        first_url = "http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=yjb"
        base_url = "http://www.job.sjtu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
        header = Util.get_header(host)
        re = Util.jedis()
        re.connect_redis()
        req = requests.Session()
        res = req.get(headers=header, url=first_url).content.decode("utf-8")
        table_name = "sjtu_company_info"
        page_num = 39
        self.parse_info(res, table_name, 14, 64, 1)

        # 解析数据
        self.get_rescruit(base_url, req, header, table_name, page_num, 14, 64, 1)
        # 在大学列表里新增表名
        self.re.add_university(table_name)

        # 保存到json文件
        self.re.add_to_file(table_name)

    def get_rescruit(self, base_url, req, header, table_name, page_num, index_begin, index_end, company_index):
        for i in range(1, page_num):
            url = base_url + str(i)
            print(url)
            res = req.get(headers=header, url=url)
            content = res.content.decode("utf-8")
            self.parse_info(content, table_name, index_begin, index_end, company_index)

    def parse_info(self, content, table_name, index_begin, index_end, company_index):
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
                print(company)
                self.re.save_info(table_name, date, company_name)
            except IndexError:
                print(len(company_info))
                continue
            except ConnectionError as e:
                self.re.print_redis_error(e)
                continue
            except BaseException as e:
                self.re.handle_error(e, table_name)

if __name__ == '__main__':
    recruit = Recruitment()
    recruit.get_scu_recruit()
    # recruit.get_sjtu_rescruit()



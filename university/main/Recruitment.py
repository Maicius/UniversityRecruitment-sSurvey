# coding = utf-8
import re
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


# 上海交通大学与四川大学的就业网是一个模板
pattern = re.compile('[0-9]+-[0-9][0-9]-[0-9][0-9]')

class Recruitment(object):

    def __init__(self):
        self.re = jedis.jedis()
        self.re.connect_redis()

    # 获取四川大学宣讲会信息
    def get_scu_recruit(self):
        table_name = "scu_company_info"
        host = 'jy.scu.edu.cn'
        referer = "http://jy.scu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx"
        base_url = "http://jy.scu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
        url = "http://jy.scu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage=0"
        self.re.clear_list(table_name)
        req = requests.Session()
        scu_header = util.get_header(host)
        scu_header['referer'] = referer
        res = req.get(headers=scu_header, url=referer)
        content = res.content.decode("utf-8")
        index_begin = 8
        index_end = 28
        page_num = self.get_page_num(content)
        self.get_rescruit(base_url, req, scu_header, table_name, page_num, index_begin, index_end, 2)
        self.re.add_university(table_name)
        self.re.add_to_file(table_name)

    # 获取上海交通大学就业信息
    def get_sjtu_rescruit(self):
        host = "www.job.sjtu.edu.cn"
        first_url = "http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=yjb"
        base_url = "http://www.job.sjtu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage="
        header = util.get_header(host)
        self.re.clear_list("sjtu_company_info")
        req = requests.Session()
        res = req.get(headers=header, url=first_url).content.decode("utf-8")
        table_name = "sjtu_company_info"
        page_num = 39
        page_num = self.get_page_num(content=res)
        # 解析数据
        self.get_rescruit(base_url, req, header, table_name, page_num, 14, 64, 1)
        # 在大学列表里新增表名
        self.re.add_university(table_name)

        # 保存到json文件
        self.re.add_to_file(table_name)

    def get_rescruit(self, base_url, req, header, table_name, page_num, index_begin, index_end, company_index):
        for i in range(0, page_num):
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
                # 在存储之前匹配一下日期格式是否正确，避免在最后一页时存储垃圾数据
                if pattern.match(date):
                    self.re.save_info(table_name, date, company_name)
            except IndexError:
                print(len(company_info))
                continue
            except ConnectionError as e:
                self.re.print_redis_error(e)
                continue
            except BaseException as e:
                self.re.handle_error(e, table_name)

    # 获取总页数
    def get_page_num(self, content):
        num = re.findall('(/&nbsp;[1-9]+&nbsp;页)', content)
        num = re.findall('[1-9]+', num[0])
        try:
            page_num = int(num[0])
            return page_num
        except BaseException as e:
            print("Failed to find total page num =================================")
            print(e)
            print("=================================")
            return


if __name__ == '__main__':
    recruit = Recruitment()
    recruit.get_scu_recruit()
    recruit.get_sjtu_rescruit()



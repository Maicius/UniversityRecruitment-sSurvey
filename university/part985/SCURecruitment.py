# coding = utf-8
import re
from bs4 import BeautifulSoup

from jedis import jedis

table_name = 'scu_company_info'
pattern = re.compile('[0-9]+-[0-9][0-9]-[0-9][0-9]')


def get_scu_recruit():
    f = open('scu_jy.html', 'r', encoding='utf-8')
    data = f.read()
    redis = jedis.jedis()
    redis.clear_list(table_name)
    parse_info(data, redis, 8, 5300)
    redis.add_university(table_name)
    redis.add_to_file(table_name)

def parse_info(content, re, index_begin, index_end):
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
            company_name = infos[2].strip()
            print(company)
            # 在存储之前匹配一下日期格式是否正确，避免在最后一页时存储垃圾数据
            if pattern.match(date):
                re.save_info(table_name, date, company_name)
        except IndexError:
            print(len(company_info))
            continue
        except ConnectionError as e:
            re.print_redis_error(e)
            continue
        except BaseException as e:
            re.handle_error(e, table_name)

if __name__ == '__main__':
    get_scu_recruit()
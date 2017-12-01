# 北京师范大学的url中带有？号，不知道是不是动态网页，刚开始分析的时候发现：点击下一页，url并不会发生改变，然后到google浏览器中查看network，发现真正
# 真正request的不是http://career.bnu.edu.cn/front/channel.jspa?channelId=764#，这个可能是它的一个框架吧，然后真正的数据应该在
# http://career.bnu.edu.cn/front/zp_query/zphQuery.jspa?paramMap.xxlx=1&page.curPage=1   这个网页里面

# @author 刘航

import requests
import json
from datetime import datetime
from jedis import jedis
from util import util

table_name = "bnu_company_info"  # 北京师范大学


def get_bnu_recuit():
    print("开始获取北京师范大学数据=====================")
    url = "http://career.bnu.edu.cn/front/zp_query/zphQuery.jspa?"
    host = "career.bnu.edu.cn"
    headers = util.get_header(host=host)
    redis = jedis.jedis()
    redis.clear_list(table_name)
    for i in range(1, 82):  # 一共81页
        try:
            params = {'paramMap.xxlx': '1', 'page.curPage': '%d' % i}
            html = requests.get(url=url, headers=headers, params=params).json()  # json 数据
            parse_info(html, redis)
        except BaseException as e:
            util.format_err(e)
        finally:
            print('获取北京师范大学第 %d 页(共81页)数据完成' % i)
    redis.add_university(table_name)  # 添加学校到github中
    redis.add_to_file(table_name)  # 添加表到文件中


def parse_info(html, redis):
    for n in range(len(html['data'])):
        try:
            timestamp = html['data'][n]['startTime'] / 1000
            date = str(datetime.fromtimestamp(timestamp).date())
            company_name = html['data'][n]['name']
            print(date, company_name)
            redis.save_info(table_name, date, company_name)
        except BaseException as e:
            util.format_err(e)
            continue


if __name__ == '__main__':
    get_bnu_recuit()

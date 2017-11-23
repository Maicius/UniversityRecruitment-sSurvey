# coding=utf-8
import requests
import json
from jedis import jedis


# 获取电子科技大学数据
def get_data(page, re, table_name):
    query_data = {
        "page": str(page),
        "time_type": 1
    }
    s = requests.session()
    query_url = "http://www.jiuye.org/new/sys/fore.php?op=listRecruit"
    content = s.post(query_url, data=query_data).text
    json_data = json.loads(content)['data']
    data = map(lambda x: dict(date=x["rec_time"][0:10], company_name=x["rec_enter_name"]), json_data)
    re.save_list(table_name, data)


def get_uestc_recruit():
    table_name = "uestc_company_info"
    print(table_name)
    re = jedis.jedis()
    re.clear_list(table_name)
    max_page_num = 407
    try:
        for i in range(1, max_page_num):
            get_data(i, re, table_name)
            print("page " + str(i) + " done!")
    except BaseException as e:
        # 意外退出时保存数据到文件
        re.handle_error(e, table_name)
    # 保存到文件
    re.add_to_file(table_name)
    # 在大学列表里增加学校名
    re.add_university(table_name)


if __name__ == "__main__":
    get_uestc_recruit()

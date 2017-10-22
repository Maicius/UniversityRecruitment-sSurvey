# coding = utf-8
# 获取清华大学宣讲会信息
# 清华大学的很多招聘会以 "就业洽谈会"的形式批量进行，需要另外计算
import json
import requests
from bs4 import BeautifulSoup
from Util import connect_redis, get_short_date


def get_tsinghua_recruit():
    base_url = "http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/jrqzph?callback=jQuery18303533298941862095_1508665403743&_=1508665403779"
    list_url = "http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?&callback=&_=&rq="
    req = requests.Session()
    res = req.get(url=base_url)
    content = res.content.decode("utf-8")
    th_infos = content.split("[")[1]
    th_info = th_infos.split("]")[0]
    th_info = "[" + th_info + "]"
    json_info = json.loads(th_info)
    th_info_dict = []

    # 去重
    item_name = ""
    for item in json_info:
        if item['zphmc'] != item_name:
            th_info_dict.append(item)
            item_name = item['zphmc']
        else:
            continue
    re = connect_redis()
    for item in th_info_dict:
        # 计算就业洽谈会的参展公司
        if item['zphmc'].find("就业洽谈会") != -1:
            rq = get_short_date(item['qsrq'])
            print(rq)
            company_list = req.get(url=list_url + str(rq)).content.decode("utf-8")
            json_company_list = json.loads(company_list[1:len(company_list) - 1])
            for info in json_company_list:
                if info['bt'].find("就业洽谈会") != -1:
                    zphid = info['zphid']
                    company_list_detail = parse_tsinghua_info(zphid)
                    company_list_dict = {'qsrq': item['qsrq'], 'zhpmc': company_list_detail}
                    re.lpush("th_company_info", company_list_dict)
                else:
                    continue
        else:
            re.lpush("th_company_info", item)


def parse_tsinghua_info(zphid):
    zphid_url = "http://career.cic.tsinghua.edu.cn/xsglxt/f/jyxt/anony/dzxDetails?zphid=" + str(zphid)
    detail = requests.get(zphid_url).content.decode("utf-8")
    soup = BeautifulSoup(detail, "html5lib")
    try:
        company_list_detail = soup.find_all("td")[13].text
    except IndexError:
        print("zphid_url")
        print(len(soup.find_all("td")))
        company_list_detail = ""
    return company_list_detail



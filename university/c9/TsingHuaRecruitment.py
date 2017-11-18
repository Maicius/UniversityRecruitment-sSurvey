# coding = utf-8
import json
import requests
from bs4 import BeautifulSoup
from jedis import jedis
from util import util


# 获取清华大学宣讲会信息
# 清华大学的很多招聘会以 "就业洽谈会"的形式批量进行，需要另外计算
def get_tsinghua_recruit():
    print("THU Begin ===================================================")
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
    re = jedis.jedis()
    re.connect_redis()
    for item in th_info_dict:
        # 计算就业洽谈会的参展公司
        if item['zphmc'].find("就业洽谈会") != -1:
            rq = util.get_short_date(item['qsrq'])
            print(rq)
            company_list = req.get(url=list_url + str(rq)).content.decode("utf-8")
            json_company_list = json.loads(company_list[1:len(company_list) - 1])
            for info in json_company_list:
                if info['bt'].find("就业洽谈会") != -1:
                    zphid = info['zphid']
                    company_list_detail = parse_tsinghua_info(zphid).split("\t\t\t\t\t\t\t\t\t\t\t\t")
                    # company_list_dict = []
                    for company in company_list_detail:
                        if company != "\n" and company != "\n\t" and company != "\t" and company != "\t\n" and company != "":
                            # company_list_dict.append({'date': item['qsrq'], 'company': company.strip()})
                            re.save_info("thu_company_info", item['qsrq'], company.strip())

                            # re.save_infos("thu_company_info", company_list_dict)
                else:
                    continue
        else:
            re.save_info("thu_company_info", item['qsrq'], item['zphmc'])

    re.add_university("thu_company_info")
    re.add_to_file("thu_company_info")
    print("THU Finish ===================================================")


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


if __name__ == '__main__':
    get_tsinghua_recruit()

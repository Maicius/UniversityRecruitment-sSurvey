# coding = utf-8
# 中国民营企业500强
import requests
from bs4 import BeautifulSoup
from analysis.SmartCountTop500 import AnalysisTop500
from jedis import jedis

private_table_name = "China_private_company_top500"
manufacture_table_name = "China_manufacture_company_top500"
service_table_name = "China_service_company_top100"


def get_china_private_top500(url, table_name):
    analysis = AnalysisTop500()
    res = requests.get(url=url).content.decode("utf-8")
    soup = BeautifulSoup(res, "html5lib")
    company_list = soup.find_all("td", attrs={"width": "130"})
    re = jedis.jedis()
    for i in range(1, len(company_list)):
        try:
            print("========")
            company_name = company_list[i].text.strip()
            short_names = analysis.get_jieba_fenci(company_name)
            re.save_info(table_name, company_name, short_names)
        except BaseException as e:
            print("Error ========")
            print(e)
    analysis.add_to_file(table_name)
    print(table_name + " 完成")


def China_private_company_infos():
    url = "http://www.cbt.com.cn/sszx/6482.html"
    get_china_private_top500(url, private_table_name)

    url2 = "http://www.cbt.com.cn/sszx/6484.html"
    get_china_private_top500(url2, manufacture_table_name)

    url3 = "http://www.cbt.com.cn/sszx/6485.html"
    get_china_private_top500(url3, service_table_name)

if __name__ == '__main__':
    China_private_company_infos()

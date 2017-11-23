# coding = utf-8
# 中国民营企业500强
import requests
from bs4 import BeautifulSoup
from analysis.SmartCountTop500 import AnalysisTop500


def get_china_private_top500():
    url = "http://www.cbt.com.cn/sszx/6482.html"
    analysis = AnalysisTop500()
    res = requests.get(url=url).content.decode("utf-8")
    soup = BeautifulSoup(res, "html5lib")
    company_list = soup.find_all("td", attrs={"width": "130"})
    for i in range(1, len(company_list)):
        print("========")
        print(i)
        company_name = company_list[i].text.strip()
        short_names = analysis.get_jieba_fenci(company_name)
    analysis.add_to_file("CHina_private_company_top500")
    print("获取中国民营企业500强完成")

if __name__ == '__main__':
    get_china_private_top500()

import re
import requests
from bs4 import BeautifulSoup
from analysis.SmartCountTop500 import AnalysisTop500
# 获取咨询行业北美50强、欧洲25强、亚太10强
from jedis import jedis


def get_consult_top100():
    url = 'https://www.sohu.com/a/160219346_169875'
    content = requests.get(url).content.decode("utf-8")
    soup = BeautifulSoup(content, "html5lib")
    company_list = soup.find_all('p')
    com_info = []
    analysis = AnalysisTop500()
    re = jedis.jedis()
    table_name = "best_consulting_company_info"
    for i in range(8, 99):
        info = company_list[i].text.strip()
        if info.find('.') != -1:
            com_info.append(info)
            # print(info)
    print(len(com_info))
    for i in range(len(com_info)):
        print("=========================================")
        print(i)
        print(com_info[i])

        if i < 10 or (50 <= i < 59) or (75 <= i < 86):
            com_info[i] = com_info[i][2: -5].strip()
        else:
            com_info[i] = com_info[i][3: -5].strip()
        print(com_info[i])
    # 结巴分词
    for item in com_info:
        short_names = analysis.get_jieba_fenci(item)
        re.save_dict(table_name, data=dict(company_name=item, short_name=short_names))
    analysis.add_to_file(table_name)
    print("获取咨询行业各种排名完成")


if __name__ == '__main__':
    get_consult_top100()

import requests
from bs4 import BeautifulSoup
from analysis.SmartCountTop500 import AnalysisTop500
from jedis import jedis


def get_investment_top100():
    analysis = AnalysisTop500()
    url = 'http://www.sohu.com/a/165350436_499106'
    res = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(res, 'html5lib')
    company_list = soup.find_all('td')
    table_name = 'investment_top100'
    re = jedis.jedis()
    re.clear_list(table_name)
    for i in range(5, len(company_list), 5):
        company_name = company_list[i + 1].text.strip()
        short_names = analysis.get_jieba_fenci(company_name)
        re.save_info(table_name, company_name, short_names)
    analysis.add_to_file(table_name)
    print(table_name + '完成')


if __name__ == '__main__':
    get_investment_top100()
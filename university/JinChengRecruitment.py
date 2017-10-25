# coding = utf-8
import requests
from bs4 import BeautifulSoup
from Util import Util


#获取四川大学锦城学院就业信息,纯静态网页
def get_jincheng_recruit():
    base_url = "http://www.scujcc.com.cn/channels/229"
    req = requests.Session()
    content = req.get(base_url + ".html").content.decode("utf-8")
    re = Util.jedis()
    re.connect_redis()
    parse_jincheng(content, re)
    for i in range(2, 99):
        print(i)
        url = base_url + "_" + str(i) + ".html"
        content = req.get(url).content.decode("utf-8")
        parse_jincheng(content, re)
    re.add_university("jincheng")
    print("finish")


def parse_jincheng(content, re):
    soup = BeautifulSoup(content, "html5lib")
    infos = soup.find_all("span")
    for i in range(2, 31, 2):
        info = {'date': infos[i + 1].text, 'company': infos[i].text}
        print(info)
        re.save_info("jincheng_company_info", infos[i + 1].text, infos[i].text)


if __name__ == '__main__':
    get_jincheng_recruit()
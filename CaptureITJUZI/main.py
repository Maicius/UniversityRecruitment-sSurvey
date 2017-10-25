import json
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from Jedis import jedis


def parse_info(table_name, json_re):
    try:
        json_data2 = json_re['juzi_company']
        for data in json_data2['detail']:
            # data = json.loads(data)
            com_id = data['com_id']
            com_name = data['com_name']
            com_industry = data['tag_name']
            header3['referer'] = "http://radar.itjuzi.com/company/" + str(com_id)
            detail_url = "http://radar.itjuzi.com/company/getinvchartdata/" + str(com_id)
            money_res = req.post(url=detail_url, headers=header3).content.decode("unicode_escape")
            money_res = json.loads(money_res)
            if money_res['msg'] == '暂无数据':
                re.save_info(table_name, com_name, com_industry)
            if money_res['msg'] == '请求成功':
                data = money_res['data']
                total_money = data['total']
                finanacing = []
                for item in data['round']:
                    time = item['time']
                    money = item['money']
                    finanacing.append({"融资时间": time, "融资金额": money})
                # 继续查询投资人
                people_url = "http://radar.itjuzi.com/company/getgrapdata/" + str(com_id)
                people_res = req.post(url=people_url, headers=header3).content.decode("unicode_escape")
                people_res = json.loads(people_res)
                data = people_res['data']
                financing_people = []
                for item in data:
                    if item['category'] == 7 or item['category'] == 6:
                        financing_people.append(item['name'])
                re.save_info(table_name, com_name, com_industry, finanacing, total_money,
                             financing_people)
    except JSONDecodeError:
        print("Error")
        pass

def get_intelli_data():
    # 智能驾驶
    # url2 = "https://www.itjuzi.com/search?word=%E6%99%BA%E8%83%BD%E9%A9%BE%E9%A9%B6"
    # url3 = "https://www.itjuzi.com/search/more?word=%E6%99%BA%E8%83%BD%E9%A9%BE%E9%A9%B6&type=juzi_company&page="
    # header2['referer'] = url2
    # more_traffic_url = url3
    # 智能交通
    # intelli_traffic_url = "https://www.itjuzi.com/search?word=%E6%99%BA%E8%83%BD%E4%BA%A4%E9%80%9A"
    # header2['referer'] = "https://www.itjuzi.com/search?word=%E6%99%BA%E8%83%BD%E4%BA%A4%E9%80%9A"
    # more_traffic_url = "https://www.itjuzi.com/search/more?word=%E6%99%BA%E8%83%BD%E4%BA%A4%E9%80%9A&type=juzi_company&page="

    # # 自动驾驶
    # url2 = "https://www.itjuzi.com/search?word=%E8%87%AA%E5%8A%A8%E9%A9%BE%E9%A9%B6"
    # url3 = "https://www.itjuzi.com/search/more?word=%E8%87%AA%E5%8A%A8%E9%A9%BE%E9%A9%B6&type=juzi_company&page="

    # 无人驾驶
    url2 = "https://www.itjuzi.com/search?word=%E6%97%A0%E4%BA%BA%E9%A9%BE%E9%A9%B6"
    url3 = "https://www.itjuzi.com/search/more?word=%E6%97%A0%E4%BA%BA%E9%A9%BE%E9%A9%B6&type=juzi_company&page="
    header2['referer'] = url2
    more_tr_url = url3 + str(1)
    tr_res = req.get(url=more_tr_url, headers=header2)
    content = tr_res.content.decode('unicode_escape')
    json_data = json.loads(content)
    parse_info("driving_without_man", json_data)
    length = int(json_data['juzi_company']['total'] / 15) + 1
    print("length:" + str(length))
    for i in range(2, 30):
        print(i)
        url = more_url + str(i)
        res1 = req.get(url=url, headers=header2).content.decode('unicode_escape')
        print(res1)
        json_res = json.loads(res1)
        parse_info("driving_without_man", json_res)


def get_car_net():
    more_url = "https://www.itjuzi.com/search/more?word=%E8%BD%A6%E8%81%94%E7%BD%91&type=juzi_company&page="
    more_url = more_url + str(1)
    res = req.get(url=more_url, headers=header2)
    content = res.content.decode('unicode_escape')
    json_data = json.loads(content)
    parse_info("car_net", json_data)
    length = int(json_data['juzi_company']['total'] / 15) + 1
    print("length:" + str(length))
    for i in range(2, 20):
        print(i)
        url = more_url + str(i)
        res = req.get(url=url, headers=header2).content.decode('unicode_escape')
        print(res)
        json_res = json.loads(res)
        parse_info("car_net", json_res)

if __name__ == '__main__':
    # 车联网
    base_url = "https://www.itjuzi.com/search?word=%E8%BD%A6%E8%81%94%E7%BD%91"

    header = {
        'host': "www.itjuzi.com",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'
    }
    header2 = {
        'host': "www.itjuzi.com",
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'referer': 'https://www.itjuzi.com/search?word=%E8%BD%A6%E8%81%94%E7%BD%91'
    }
    more_url = "https://www.itjuzi.com/search/more?word=%E8%BD%A6%E8%81%94%E7%BD%91&type=juzi_company&page="
    req = requests.Session()
    res = req.get(headers=header, url=base_url)
    content = res.content.decode("unicode_escape")
    # print(content)
    soup = BeautifulSoup(content, "html5lib")
    re = jedis()
    # company_list = soup.find_all("li")
    # for item in company_list:
    #     print(item.text)
    header3 = {
        'host': "radar.itjuzi.com",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'referer': 'http://radar.itjuzi.com/company/16436',
        'Cookie': 'Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1508856141; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1508864732; gr_user_id=7cbc4c46-b927-47c6-aa60-a0e178251c25; gr_session_id_eee5a46c52000d401f969f4535bdaa78=38434975-c893-422c-baef-7d957d08a58e; _ga=GA1.2.1387165269.1508856143; _gid=GA1.2.1168233932.1508856143; acw_tc=AQAAAAOV9Ud0gQoADXHS3uTwiEBRvTNa; user-radar.itjuzi.com=%7B%22n%22%3A%22%5Cu9ea6%5Cu5b50%22%2C%22v%22%3A2%7D; pgv_pvi=3755104256; pgv_si=s1401233408; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1508859785; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1508864746; session=416ead74a07ffc77dafcad79323f6ea8a3592896; identity=18996720676%40test.com; remember_code=X9TNJOCurP; unique_token=457899; _gat=1; gr_cs1_38434975-c893-422c-baef-7d957d08a58e=user_id%3A457899'    }
    # get_car_net()
    get_intelli_data()
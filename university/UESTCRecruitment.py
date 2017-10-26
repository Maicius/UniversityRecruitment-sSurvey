#coding=utf-8
import requests
import json


def get_data(page):
    query_data = {
        "page": str(page),
        "time_type": 1
    }
    s = requests.session()
    query_url = "http://www.jiuye.org/new/sys/fore.php?op=listRecruit"
    content = s.post(query_url, data=query_data).text
    json_data = json.loads(content)['data']
    data = map(lambda x: dict(date=x["rec_time"].encode('utf-8'), company_name=x["rec_enter_name"].encode('utf-8')), json_data)
    return data


if __name__ == "__main__":
    data = []
    for i in range(1, 407):
        data.extend(get_data(i))
        print "page "+str(i)+" done!"
    with open("uestc_data.json", "w") as f:
        json.dump(data, f)




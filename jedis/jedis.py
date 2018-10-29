# coding=utf-8
import json
import traceback
import redis


# 封装redis的操作，统一数据接口
# 为没有安装redis的用户提供保存到json文件的接口
class jedis(object):
    def __init__(self):
        # 使用redis保存数据，如果没有redis须注释掉这两句代码
        # 使用json文件保存数据
        self.data_array = []
        self.host = "134.175.58.80"
        self.port = "6379"
        self.re = self.get_re()

    # 返回一个原生的redis对象
    def get_re(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=6379, decode_responses=True, password=110110)
            return redis.StrictRedis(connection_pool=pool)
        except BaseException as e:
            self.print_redis_error(e)

    def connect_redis(self):
        return self.re

    # 保存数据，将传入的date 和company_name 格式化为字典再保存
    def save_info(self, name, date, company_name):
        data = {"date": date, "company_name": company_name}
        self.save_dict(name, data)

    # 保存字典格式的数据
    def save_dict(self, name, data):
        try:
            # 在插入数据之前将所有对引号替换为中文引号，避免在redis中被替换
            # 但是由于这两句十分的慢，所以一般注释掉
            data['company_name'] = data['company_name'].replace('\"', '”')
            data['company_name'] = data['company_name'].replace('\'', '”')
            # 如果不使用redis也要注释掉这句
            self.re.lpush(name, data)
            # pass
        except BaseException as e:
            self.print_redis_error(e)
        # 将数据缓存到data_array中，最终保存数据
        self.data_array.append(data)

    # 保存一个列表
    def save_list(self, name, data_list):
        for item in data_list:
            self.save_dict(name, item)

    def save_infos(self, name, item):
        try:
            self.re.lpush(name, item)
        except BaseException as e:
            self.print_redis_error(e)

    def save_company_info(self, name, company_rank, company_name, company_industry, company_contry, company_profit,
                          company_people_num, company_type):
        try:
            com_data = {"company_rank": company_rank, "company_name": company_name, "company_contry": company_contry,
                        "company_industry": company_industry, "company_profit": company_profit,
                        "company_people_num": company_people_num, "company_type": company_type}
            self.re.lpush(name,
                          com_data)
            self.data_array.append(com_data)
        except BaseException as e:
            self.add_to_file(name)
            self.print_redis_error(e)

    # 维持一个大学列表，记录每个大学list的名称
    def add_university(self, name):
        university_list = self.get_university_list()
        if name not in university_list:
            self.re.lpush("university", name)

    # 保存到文件
    def add_to_file(self, name):
        # for py3
        with open('../../data/university_data/' + name + '.json', 'w', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
            # for py2
            # with open('../data/' + name + '.json', 'w+') as w:
            #     json.dump(self.data_array, w, ensure_ascii=False)

    def add_to_file_tail(self, name):
        # for py3
        with open('../../data/university_data/' + name + '.json', 'w+', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
            # for py2
            # with open('../data/' + name + '.json', 'w+') as w:
            #     json.dump(self.data_array, w, ensure_ascii=False)

    def add_to_file_local(self, name):
        # for py3
        with open(name + '.json', 'w+', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
            # for py2
            # with open('../data/' + name + '.json', 'w+') as w:
            #     json.dump(self.data_array, w, ensure_ascii=False)

    # 测试
    def test_add_to_file(self):
        self.add_to_file("py2_test")

    # 测试
    def test_add_to_file_tail(self):
        self.add_to_file_tail("py2_test")

    def get_university_list(self):
        return self.re.lrange("university", 0, -1)

    def handle_error(self, e, name):
        print("Unexpected Error")
        print("The program will save the data and exit")
        # 程序意外退出时保存文件
        self.add_to_file(name)
        msg = traceback.format_exc(e)
        print(msg)

    def clear_list(self, name):
        self.re.ltrim(name, -1, 0)

    def print_redis_error(self, e):
        msg = traceback.format_exc(e)
        print(msg)
        print("redis failed to connect, please check redis config")
        print("now the data would to save into json file only")


if __name__ == '__main__':
    # re = jedis()
    # re.connect_redis()
    # re.add_university("scu_company_info")
    # re.add_university("thu_company_info")
    # re.add_university("nju_company_info")
    # re.add_university("sjtu_company_info")
    # re.add_university("jincheng_company_info")
    # re.add_university("lzu_company_info")
    # re.add_university("ustc_company_info")
    # re.add_university("cufe_company_info")
    # re.add_university("cqu_company_info")
    # re.add_university("hust_company_info")
    # str1 = "Oct 19, 2017 12:00:00 AM"
    # # str1 = str1[0:12]
    # time = get_standard_date(str1)
    # print(time)
    re = jedis()
    re.test_add_to_file_tail()

import redis


class jedis(object):
    def __init__(self):
        # 使用redis保存数据，如果没有redis须注释掉这两句代码

        # 使用json文件保存数据
        self.data_array = []
        self.host = "127.0.0.1"
        self.port = "6379"
        self.re = self.get_re()

    # 返回一个原生的redis对象
    def get_re(self):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)
        re = redis.StrictRedis(connection_pool= pool)
        return re

    def connect_redis(self):
        return self.re


    def save_info(self, name, company_name, industry, financing="", total_money="", people="无"):

        data = {"company_name": company_name, 'industry': industry,
                "financing": financing, 'total_money':total_money, 'people':people}
        print(data)
        self.re.lpush(name, data)

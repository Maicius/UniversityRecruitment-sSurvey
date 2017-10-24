import redis

from Util import Util

class AnalysisTop500(object):
    def __init__(self):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)
        self.re = redis.StrictRedis(connection_pool=pool)

    def get_university_list(self):
        bytes_list = self.re.lrange("scu_company_info", 0, -1)
        return bytes_list


if __name__ == '__main__':
    analysis = AnalysisTop500()
    university_list = analysis.get_university_list()
    print(" ".join(university_list))
import json

from jedis import jedis


class AnalysisTop500(object):
    def __init__(self):
        self.re = jedis.jedis().get_re()
        self.USA_company_list = []
        self.China_company_list = []
        self.World_company_list = []

    def get_university_list(self):
        return self.re.lrange("university", 0, -1)

    def get_top_500_list(self):
        company_info = self.re.lrange("company_info", 0, -1)

        for item in company_info:
            try:
                item = item.replace('\'', '"')
                item = item.replace('==', '\'')
                print(item)
                item = json.loads(item)
                company_name = item['company_name']
                company_name = company_name.replace('++', '\"')
                company_type = item['company_type']
                print(company_name)
                if company_type == "USATop500":
                    self.USA_company_list.append(company_name)
                elif company_type == "ChinaTop500":
                    self.China_company_list.append(company_name)
                elif company_type == "WorldTop500":
                    self.World_company_list.append(company_name)
            except BaseException as e:
                print("error=============================================================")
                print(item)
                print(e)
                print("error=============================================================")
                continue

    def get_china_top_500(self, university):
        university_company_list = self.re.lrange(university, 0, -1)
        self.get_top_500_list()
        for university in university_company_list:
            if university in self.China_company_list:
                print(university)


if __name__ == '__main__':
    analysis = AnalysisTop500()
    university_list = analysis.get_university_list()
    analysis.get_top_500_list()
    print(" ".join(university_list))
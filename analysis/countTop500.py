import json

from jedis import jedis
import jieba

waste_words = "有限公司 公司 集团 股份 2017 2016 2015 宣讲会 招聘会 招聘 正式启动 "

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
        university_list = self.re.lrange(university, 0, -1)

        self.get_top_500_list()
        self.get_university_company_name(university_list)
        for university in university_list:
            if university in self.China_company_list:
                pass

    def get_university_company_name(self, university_list):
        for university in university_list:
            self.get_company_short_name(university)

    def get_company_short_name(self, university):
        company_list = self.re.lrange(university, 0, -1)
        for company in company_list:
            try:
                company = company.replace('\'', '"')
                company = json.loads(company)
                company_name = company['company_name']
                short_names = jieba.cut(company_name, cut_all=False)
                print("===============")
                print(company_name + ":" + " ".join(short_names))

            except BaseException as e:
                print("error=============================================================")
                print(company)
                print("error=============================================================")
                continue

if __name__ == '__main__':
    analysis = AnalysisTop500()
    analysis.get_top_500_list()
    analysis.get_china_top_500("university")
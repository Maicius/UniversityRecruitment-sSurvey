from Util import Util


class AnalysisTop500(object):
    def __init__(self):
        self.re = Util.jedis().get_re()
        self.USA_company_dict = {}
        self.China_company_dict = {}
        self.World_company_dict = {}

    def get_university_list(self):
        return self.re.lrange("university", 0, -1)

    def get_top_500_list(self):
        company_info = self.re.lrange("company_info", 0, -1)
        for item in company_info:
            company_name = item['company_name']
            company_type = item['company_type']
            if company_type == "USATop500":
                self.USA_company_dict[company_name] = 1
            elif company_type == "ChinaTop500":
                self.China_company_dict[company_name] = 1
            elif company_type == "WorldTop500":
                self.World_company_dict[company_name] = 1

    def get_china_top_500(self, university):
        university_company_list = self.re.lrange(university, 0, -1)
        self.get_top_500_list()

        for item in university_company_list:
            if item in self.China_company_dict:
                print(item)


if __name__ == '__main__':
    analysis = AnalysisTop500()
    university_list = analysis.get_university_list()

    print(" ".join(university_list))
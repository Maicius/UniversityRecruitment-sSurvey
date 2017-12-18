# 根据省份对大学数据进行划分
from analysis.SmartAnalysisByName import SmartAnalysisByName
from constant.constant import UNIVERSITY_INFO


class SmartAnalysisByAddr(SmartAnalysisByName):
    def __init__(self):
        SmartAnalysisByName.__init__(self)
        # C9\985\211分为一类
        # 数据格式为[{'城市':[('大学', '数量')]}]
        self.p211_up_company_city = {}
        self.p211_up_company_province = {}

        # C9\985\211
        self.p211_up_company_city_avg = []
        self.p211_up_company_province_avg = []

        # 普通一本和二本分为一类
        self.top_basic_company_city = {}
        self.top_basic_company_province = {}

        self.top_basic_company_city_avg = []
        self.top_basic_company_province_avg = []

        self.p211_up = ('C9', '985', '211')
        self.basic_top = ('一本', '二本')

    def calculate_num_by_addr(self):
        self.get_univeristy_company_list(self.get_university_list())
        for index, value in self.university_company_list_length_dict.items():
            university_short_name = index[:-len('_company_info')]
            university_province = UNIVERSITY_INFO[university_short_name][2]
            university_city = UNIVERSITY_INFO[university_short_name][3]
            university_type = UNIVERSITY_INFO[university_short_name][1]
            university_name = UNIVERSITY_INFO[university_short_name][0]
            print(index, value)
            if university_province in self.p211_up_company_province and university_type in self.p211_up:
                self.p211_up_company_province[university_province].append((university_name, value))
            elif university_province not in self.p211_up_company_province and university_type in self.p211_up:
                self.p211_up_company_province[university_province] = [(university_name, value)]

            elif university_province in self.top_basic_company_province and university_type in self.basic_top:
                self.top_basic_company_province[university_province].append((university_name, value))

            elif university_province not in self.top_basic_company_province and university_type in self.basic_top:
                self.top_basic_company_province[university_province] = [(university_name, value)]

            if university_type in self.p211_up:
                if university_city in self.p211_up_company_city:
                    self.p211_up_company_city[university_city].append((university_name, value))
                else:
                    self.p211_up_company_city[university_city] = [(university_name, value)]
            elif university_type in self.basic_top:
                if university_city in self.top_basic_company_city:
                    self.top_basic_company_city[university_city].append((university_name, value))
                else:
                    self.top_basic_company_city[university_city] = [(university_name, value)]

    def get_avg_num(self):
        self.p211_up_company_city_avg = self.calculate_avg_by_addr(self.p211_up_company_city)
        self.p211_up_company_province_avg = self.calculate_avg_by_addr(self.p211_up_company_province)
        self.top_basic_company_city_avg = self.calculate_avg_by_addr(self.top_basic_company_city)
        self.top_basic_company_province_avg = self.calculate_avg_by_addr(self.top_basic_company_province)

    # 数据为[{'城市':[('大学', '数量')]}]
    def calculate_avg_by_addr(self, info):
        result_list = []
        for index, value in info.items():
            # 一个城市或省份中的大学211以上大学或普通一二本高校的数量
            university_num = len(value)
            total_num = sum(map(lambda x: x[1], value))
            if university_num != 0:
                result_list.append((index, int(total_num/university_num)))
            else:
                result_list.append((index, 0))
        return result_list

if __name__ == '__main__':
    analysis = SmartAnalysisByAddr()
    analysis.calculate_num_by_addr()
    analysis.get_avg_num()
    print(sorted(analysis.p211_up_company_province_avg, key=lambda x: x[1], reverse=True))
    print(sorted(analysis.p211_up_company_city_avg, key=lambda x: x[1], reverse=True))
    print(sorted(analysis.top_basic_company_province_avg, key=lambda x: x[1], reverse=True))
    print(sorted(analysis.top_basic_company_city_avg, key=lambda x: x[1], reverse=True))

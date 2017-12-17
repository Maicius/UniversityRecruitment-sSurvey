# 根据省份对大学数据进行划分
from analysis.SmartAnalysisByName import SmartAnalysisByName
from constant.constant import UNIVERSITY_INFO


class SmartAnalysisByAddr(SmartAnalysisByName):
    def __init__(self):
        SmartAnalysisByName.__init__(self)
        # C9\985\211分为一类
        self.p211_up_company_city = {}
        self.p211_up_company_province = {}
        # 普通一本和二本分为一类
        self.top_basic_company_city = {}
        self.top_basic_company_province = {}
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


if __name__ == '__main__':
    analysis = SmartAnalysisByAddr()
    analysis.calculate_num_by_addr()
    print(sorted(analysis.p211_up_company_province.items(), key=lambda x: x[1], reverse=True))
    print(sorted(analysis.p211_up_company_city.items(), key=lambda x: x[1], reverse=True))
    print(sorted(analysis.top_basic_company_province.items(), key=lambda x: x[1], reverse=True))
    print(sorted(analysis.top_basic_company_city.items(), key=lambda x: x[1], reverse=True))

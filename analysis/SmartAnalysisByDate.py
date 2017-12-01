import json
from constant.constant import UNIVERSITY_INFO
from analysis.SmartAnalysisByName import SmartAnalysisByName
from util import util


# 根据日期进行分析
class SmartAnalysisByDate(SmartAnalysisByName):
    def __init__(self):
        SmartAnalysisByName.__init__(self)
        self.c9_company_date_dict = {}
        self.p985_company_date_dict = {}
        self.p211_company_date_dict = {}
        self.top_company_date_dict = {}
        self.basic_company_date_dict = {}

    def calculate_activity_degree(self):
        university_list = self.get_university_list()
        for university_table in university_list:
            university = UNIVERSITY_INFO[university_table[:-len('_company_info')]]
            company_list = self.re.lrange(university_table, 0, -1)
            if university[1] == 'C9':
                self.get_company_num_in_diff_date(company_list, self.c9_company_date_dict)
            elif university[1] == '985':
                self.get_company_num_in_diff_date(company_list, self.p985_company_date_dict)
            elif university[1] == '211':
                self.get_company_num_in_diff_date(company_list, self.p211_company_date_dict)
            elif university[1] == '一本':
                self.get_company_num_in_diff_date(company_list, self.top_company_date_dict)
            elif university[1] == '二本':
                self.get_company_num_in_diff_date(company_list, self.basic_company_date_dict)
            else:
                util.format_err(university)
        print("finish")

    def get_company_num_in_diff_date(self, company_list, result_dict):
        for company in company_list:
            try:
                company = company.replace('\'', '\"')
                company = json.loads(company)
                date_time = company['date']
                # company_name = company['company_name']
                print(date_time)
                if date_time in result_dict:
                    result_dict[date_time] += 1
                else:
                    result_dict[date_time] = 1
            except BaseException as e:
                util.format_err(e)

    def print_and_save_result2(self, result_dict, filename):
        self.data_array = []
        for key, values in result_dict.items():
            print('--------------------------------------')
            try:
                print(key, values)
                self.data_array.append(dict(name=key, value=values))
            except BaseException as e:
                util.format_err(e)
                continue
        self.save_result(filename)

if __name__ == '__main__':
    analysis_date = SmartAnalysisByDate()
    analysis_date.calculate_activity_degree()
    print("C9================================")
    analysis_date.print_and_save_result2(analysis_date.c9_company_date_dict, 'c9_company_date_result')
    print("985================================")
    analysis_date.print_and_save_result2(analysis_date.p985_company_date_dict, 'p985_company_date_result')
    print("211================================")
    analysis_date.print_and_save_result2(analysis_date.p211_company_date_dict, 'p211_company_date_result')
    print("一本================================")
    analysis_date.print_and_save_result2(analysis_date.top_company_date_dict, 'top_company_date_result')
    print("二本================================")
    analysis_date.print_and_save_result2(analysis_date.basic_company_date_dict, 'basic_company_date_result')

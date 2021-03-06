import json
from constant.constant import UNIVERSITY_INFO
from analysis.SmartAnalysisByName import SmartAnalysisByName
from util import util


# 根据日期进行分析
class SmartAnalysisByDate(SmartAnalysisByName):
    def __init__(self):
        SmartAnalysisByName.__init__(self)
        self.data_array_range = []
        self.c9_company_date_dict = {}
        self.p985_company_date_dict = {}
        self.p211_company_date_dict = {}
        self.top_company_date_dict = {}
        self.basic_company_date_dict = {}
        self.data_array_each_day_dict = {}

    def calculate_activity_degree(self):
        university_list = self.get_university_list()
        for university_table in university_list:
            university = UNIVERSITY_INFO[university_table[:-len('_company_info')]]
            company_list = self.re.lrange(university_table, 0, -1)
            if university[1] == 'C9':
                self.get_company_num_in_diff_date(company_list, self.c9_company_date_dict, "c9")
            elif university[1] == '985':
                self.get_company_num_in_diff_date(company_list, self.p985_company_date_dict, "p985")
            elif university[1] == '211':
                self.get_company_num_in_diff_date(company_list, self.p211_company_date_dict, "p211")
            elif university[1] == '一本':
                self.get_company_num_in_diff_date(company_list, self.top_company_date_dict, "top")
            elif university[1] == '二本':
                self.get_company_num_in_diff_date(company_list, self.basic_company_date_dict, "basic")
            else:
                util.format_err(university)
        self.save_date_dict()
        print("finish")

    def save_date_dict(self):
        new_data_array = []
        for time, value in self.data_array_each_day_dict.items():
            new_data_array.append(
                dict(date=util.get_standard_time_from_mktime(int(time)), c9=value['c9'], p985=value['p985'],
                     p211=value['p211'], top=value['top'], basic=value['basic']))

            self.save_result2("total_date_result", new_data_array)

    def get_2013_2017_each_day(self):
        for timestamp in range(1356969600, 1514563200, 86400):
            self.data_array_each_day_dict[str(timestamp)] = dict(c9=0, p985=0, p211=0, top=0, basic=0)

    def get_company_num_in_diff_date(self, company_list, result_dict, type):
        for company in company_list:
            try:
                company = company.replace('\'', '\"')
                company = json.loads(company)
                date_time = company['date']
                # company_name = company['company_name']
                print(date_time)
                # 将标准时间转化为时间戳
                date_time = util.get_mktime(date_time)
                if str(date_time) in result_dict:
                    result_dict[str(date_time)] += 1

                else:
                    result_dict[str(date_time)] = 1
                if str(int(float(date_time))) in self.data_array_each_day_dict:
                    self.data_array_each_day_dict[str(int(float(date_time)))][type] += 1
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
        self.data_array = sorted(self.data_array, key=lambda x: float(x['name']))
        # 表示从 2013-01-01 至2017-12-30， 步长为一天
        for item in self.data_array:
            # 2013.01.01之前的数据都不要了
            if int(float(item['name'])) < 1356969600:
                pass
            else:
                item['name'] = util.get_standard_time_from_mktime(int(float(item['name'])))
                self.data_array_range.append(item)

        # self.data_array = list(map(lambda x: util.get_standard_time_from_mktime(int(float(x['name']))), self.data_array))

        self.save_result2(filename, self.data_array_range)

    def save_result2(self, filename, data_array):
        with open('../data/result_data/' + filename + '.js', 'w', encoding='utf-8') as w:
            # json.dump(self.data_array, w, ensure_ascii=False)
            # 将json 数据转化为js的const 变量
            data_str = str(data_array).replace('\'', "\"")
            w.write("const " + filename + "=" + data_str + ';')


if __name__ == '__main__':
    analysis_date = SmartAnalysisByDate()
    analysis_date.get_2013_2017_each_day()
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

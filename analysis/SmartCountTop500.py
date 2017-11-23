# coding = utf-8
import json

import jieba
import re

from jedis import jedis


# 分析500强的另一种方法
# 对从财富网站上爬取的500强企业名单进行分词
# 去掉集团、公司等字样，并人为补充一下简称
# 比如中国石油化工集团股份有限公司的简称有： 中国石油化工、中国石化、中石化
# 使用这些简称与从各个大学上爬取的宣讲会标题进行匹配
# 匹配成功则表示该公司曾到该大学宣讲
class AnalysisTop500(object):
    def __init__(self):
        self.re = jedis.jedis().get_re()
        self.USA_company_list = []
        self.China_company_list = []
        self.World_company_list = []
        self.china_top500_dict = {}
        self.world_top500_dict = {}
        self.usa_top500_dict = {}
        self.university_company_dict = {}
        self.data_array = []
        self.china_top500_result = {}
        self.usa_top500_result = {}
        self.world_top500_result = {}

    # 主逻辑函数
    def get_univeristy_company_list(self, university_list):
        for university_table_name in university_list:
            self.china_top500_result[university_table_name] = []
            self.usa_top500_result[university_table_name] = []
            self.world_top500_result[university_table_name] = []
            company_list = self.get_2017_company_list(university_table_name)
            for company in company_list:
                try:
                    company = company['company_name']
                    # print(company)
                    # 判断中国五百强
                    for short_names in self.china_top500_dict:
                        for short_name in short_names['short_name']:
                            if company.find(short_name) != -1:
                                if short_name == '京东' and company.find('京东方') != -1:
                                    break
                                if short_name == '京东方' and company.find('北京东') != -1:
                                    break
                                if short_name == '京东' and company.find('北京东') != -1:
                                    break
                                else:
                                    # print(short_name + "-" + company)
                                    self.china_top500_result[university_table_name].append(short_name+"-" + company)
                                    break

                    # 判断是不是世界五百强
                    for short_names in self.world_top500_dict:
                        for short_name in short_names['short_name']:
                            if company.find(short_name) != -1:
                                if short_name == '京东' and company.find('京东方') != -1:
                                    break
                                if short_name == '京东方' and company.find('北京东') != -1:
                                    break
                                if short_name == '京东' and company.find('北京东') != -1:
                                    break
                                else:
                                    # print(short_name + "-" + company)
                                    self.world_top500_result[university_table_name].append(short_name+"-" + company)
                                    break

                    # 判断是不是美国五百强
                    for short_names in self.usa_top500_dict:
                        for short_name in short_names['short_name']:
                            if company.find(short_name) != -1:
                                # print(short_name + "-" + company)
                                self.usa_top500_result[university_table_name].append(short_name+"-" + company)
                                break
                except BaseException as e:
                    print("Error===================================================")
                    print(e)
                    print(company)
                    print("Error===================================================")

    # 获取大学的列表
    def get_university_list(self):
        return self.re.lrange("university", 0, -1)

    # 从文件中读取500强名单
    def get_company_short_name(self):
        with open("China_Top_500.json", 'r', encoding='utf-8') as r:
            self.china_top500_dict = json.load(r)
        with open("USA_Top_500.json", 'r', encoding='utf-8') as r:
            self.usa_top500_dict = json.load(r)
        with open("World_Top_500.json", 'r', encoding='utf-8') as r:
            self.world_top500_dict = json.load(r)
        print("Get Short Name Finish")

    # 从爬取的宣讲会标题中获取2017年度的宣讲会
    def get_2017_company_list(self, university_table_name):
        company_list = self.re.lrange(university_table_name, 0, -1)
        company_list_2017 = []
        for item in company_list:
            try:
                item = item.replace('\'', '"')
                item = json.loads(item)
                date = item['date']
                if date.find('2017') != -1:
                    company_list_2017.append(item)
            except BaseException as e:
                print("error=============================================================")
                print(university_table_name)
                print(item)
                print(e)
                print("error=============================================================")
                continue
        print("Finish to find 2017 Recruitment--" + university_table_name)
        return company_list_2017

    # 从数据库里读取500强信息（包括全名、CEO、盈利额等，但是不包括简称）
    def get_top_500_list(self):
        company_info = self.re.lrange("company_info", 0, -1)
        for item in company_info:
            try:
                item = item.replace('\'', '"')
                item = item.replace('==', '\'')
                # print(item)
                item = json.loads(item)
                company_name = item['company_name']
                company_name = company_name.replace('++', '\"')
                company_type = item['company_type']
                # print(company_name)
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

    # 利用从数据库里读取的500强信息截取公司简称
    def get_top_500_real_name(self):
        for company in self.China_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("China_Top_500_2")

        for company in self.USA_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("USA_Top_500_2")

        for company in self.World_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("World_Top_500_2")

    # 分词算法
    def get_jieba_fenci(self, company_name):
        print("================================")
        waste_words = ['控股', '股份', '有限公司', '有限', '公司', '集团', '（', '）', '资产管理', '通信', '集团股份',
                       '电子商务', '商城', '矿业集团', '信息产业', '发展股份', '控股集团', '(', ')',
                       '企业', '&', '综合']
        # waste_words = " ".join(waste_words)
        short_names = []
        english_name = re.findall('(\(.*?\))', company_name)
        if len(english_name) > 0 and len(re.findall('[\u4e00-\u9fa5]', english_name[0])) == 0:
            english_name = english_name[0][1: len(english_name[0]) - 1]
            print("english name:" + english_name)
            short_names.append(english_name)
            chinese_name = company_name[:company_name.find('(')]
        else:
            chinese_name = company_name
        print("chinese name:" + chinese_name)
        real_names = jieba.cut(chinese_name, cut_all=False)
        real_name = []
        for item in real_names:
            # print(item)
            if item not in waste_words:
                real_name.append(item)
        short_name = "".join(real_name)
        # short_name = short_name[0:short_name.find('集团') + 2]
        # short_name = short_name[0:short_name.find('公司') + 2]
        if short_name.find('公司') != -1:
            short_name = short_name[0:short_name.find('公司')]
        if short_name.find('集团') != -1:
            short_name = short_name[0:short_name.find('集团')]
        print("short_name:" + short_name)
        short_names.append(short_name)
        self.data_array.append(dict(company_name=company_name, short_name=short_names))

    # 保存到文件
    def add_to_file(self, file_name):
        # for py3
        with open(file_name + '.json', 'w', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
        self.data_array = []


if __name__ == '__main__':
    analysis = AnalysisTop500()
    # analysis.get_top_500_list()
    # analysis.get_top_500_real_name()
    analysis.get_company_short_name()
    university = analysis.get_university_list()
    analysis.get_univeristy_company_list(university_list=university)
    print("到这些学校开宣讲会的中国五百强数量================================")
    for key, values in analysis.china_top500_result.items():
        # print(key + ":" + str(len(values)) + "\n" + " ".join(values))
        print(key + ":" + str(len(values)))

    print("到这些学校开宣讲会的美国五百强================================")
    for key, values in analysis.usa_top500_result.items():
        # print(key + ":" + str(len(values)) + "\n" + " ".join(values))
        print(key + ":" + str(len(values)))

    print("到这些学校开宣讲会的世界五百强================================")
    for key, values in analysis.world_top500_result.items():
        # print(key + ":" + str(len(values)) + "\n" + " ".join(values))
        print(key + ":" + str(len(values)))

    print(analysis.china_top500_result)
    print(analysis.usa_top500_result)
    print(analysis.world_top500_result)
    print("Finish")

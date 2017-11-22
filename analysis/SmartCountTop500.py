# coding = utf-8
import json

import jieba
import re

from jedis import jedis


class AnalysisTop500(object):
    def __init__(self):
        self.re = jedis.jedis().get_re()
        self.USA_company_list = []
        self.China_company_list = []
        self.World_company_list = []
        self.china_top500_dict = {}
        self.world_top500_dict = {}
        self.usa_top500_dict = {}
        self.usa_company_str = ""
        self.china_company_str = ""
        self.world_company_str = ""
        self.university_company_dict = {}
        self.data_array = []

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

    def get_top_500_real_name(self):
        for company in self.China_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("China_Top_500")

        for company in self.USA_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("USA_Top_500")

        for company in self.World_company_list:
            self.get_jieba_fenci(company)
        self.add_to_file("World_Top_500")

    def get_jieba_fenci(self, company_name):
        print("================================")
        waste_words = ['控股', '股份', '有限公司', '有限', '公司', '集团', '（', '）', '资产管理', '通信', '集团股份',
                       '电子商务', '商城', '出版', '传媒', '矿业集团', '信息产业', '发展股份', '控股集团',
                       '企业', '&', '综合']
        # waste_words = " ".join(waste_words)

        english_name = re.findall('(\(.*?\))', company_name)
        if len(english_name) > 0 and len(re.findall('[\u4e00-\u9fa5]', english_name[0])) == 0:
            english_name = english_name[0][1: len(english_name[0]) - 1]
            print("english name:" + english_name)
            chinese_name = company_name[:company_name.find('(')]
        else:
            chinese_name = company_name
        print("chinese name:" + chinese_name)
        real_names = jieba.cut(chinese_name, cut_all=False)
        real_name = []
        for item in real_names:
            print(item)
            if item not in waste_words:
                real_name.append(item)
        short_name = "".join(real_name)
        # short_name = short_name[0:short_name.find('集团') + 2]
        # short_name = short_name[0:short_name.find('公司') + 2]
        print("short_name:" + short_name)
        self.data_array.append(dict(company_name=company_name, short_name=real_name))

    def add_to_file(self, file_name):
        # for py3
        with open(file_name + '.json', 'w', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
        self.data_array = []

    def get_university_top_500(self, university):
        university_list = self.re.lrange(university, 0, -1)
        for universe in university_list:
            university_company_list = self.re.lrange(universe, 0, -1)
            self.university_company_dict[universe].append(university_company_list)

if __name__ == '__main__':
    analysis = AnalysisTop500()
    analysis.get_top_500_list()
    analysis.get_top_500_real_name()


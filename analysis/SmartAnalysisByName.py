# encoding = utf-8
import json
import jieba
import re
from util import util
from constant.constant import UNIVERSITY_INFO
from constant.constant import COMPANY_WASTE_WORDS
from jedis import jedis


# 分析500强的另一种方法
# 对从财富网站上爬取的500强企业名单进行分词
# 去掉集团、公司等字样，并人为补充一下简称
# 比如中国石油化工集团股份有限公司的简称有： 中国石油化工、中国石化、中石化
# 使用这些简称与从各个大学上爬取的宣讲会标题进行匹配
# 匹配成功则表示该公司曾到该大学宣讲
class SmartAnalysisByName(object):
    def __init__(self):
        self.re = jedis.jedis().get_re()
        self.data_array = []
        self.university_company_dict = {}
        self.count = 0
        self.USA_company_list = []
        self.China_company_list = []
        self.World_company_list = []

        self.China_top500_dict = {}
        self.world_top500_dict = {}
        self.usa_top500_dict = {}

        self.manufacture_top500_dict = {}
        self.China_private_top500_dict = {}
        self.world_investment_top100_dict = {}
        self.world_consult_top75_dict = {}
        self.China_service_top100_dict = {}
        self.China_it_top100_dict = {}

        # 记录每个大学某年度的宣讲会总数量
        self.university_company_list_length_dict = {}
        # 中国500强结果
        self.China_top500_result = {}
        # 美国五百强结果
        self.usa_top500_result = {}
        # 世界五百强结果
        self.world_top500_result = {}
        # 中国民营企业制造业500强
        self.China_manufacture_top500_result = {}
        # 中国私有企业500强
        self.China_private_top500_result = {}
        # 世界投资机构100强
        self.world_investment_top100_result = {}
        # 中国互联网企业100强
        self.China_it_top100_result = {}
        # 中国服务业100强
        self.China_service_top100_result = {}
        # 咨询行业北美50强、欧洲25强、亚太10强
        self.world_consult_top75_result = {}

    # 主逻辑函数
    def get_univeristy_company_list(self, university_list):
        for university_table_name in university_list:
            self.China_top500_result[university_table_name] = []
            self.usa_top500_result[university_table_name] = []
            self.world_top500_result[university_table_name] = []
            self.China_service_top100_result[university_table_name] = []
            self.world_consult_top75_result[university_table_name] = []
            self.world_investment_top100_result[university_table_name] = []
            self.China_manufacture_top500_result[university_table_name] = []
            self.China_it_top100_result[university_table_name] = []
            self.China_private_top500_result[university_table_name] = []
            company_list, university_company_list_length = self.get_2017_company_list(university_table_name)
            self.university_company_list_length_dict[university_table_name] = university_company_list_length
            for company in company_list:
                try:
                    article_title = company['company_name']
                    # print(company)
                    # 判断中国五百强
                    self.get_company_type_num(article_title, self.China_top500_result[university_table_name],
                                              self.China_top500_dict)
                    # 判断是不是世界五百强
                    self.get_company_type_num(article_title, self.usa_top500_result[university_table_name],
                                              self.usa_top500_dict)

                    # 判断是不是美国五百强
                    self.get_company_type_num(article_title, self.world_top500_result[university_table_name],
                                              self.world_top500_dict)

                    # 判断是不是咨询业75强
                    self.get_company_type_num(article_title, self.world_consult_top75_result[university_table_name],
                                              self.world_consult_top75_dict)

                    # 判断是不是投资机构100强
                    self.get_company_type_num(article_title, self.world_investment_top100_result[university_table_name],
                                              self.world_investment_top100_dict)

                    # 判断是不是中国服务业100强
                    self.get_company_type_num(article_title, self.China_service_top100_result[university_table_name],
                                              self.China_service_top100_dict)

                    # 判断是不是中国制造业500强
                    self.get_company_type_num(article_title,
                                              self.China_manufacture_top500_result[university_table_name],
                                              self.manufacture_top500_dict)
                    # 判断是不是中国IT业100强
                    self.get_company_type_num(article_title,
                                              self.China_it_top100_result[university_table_name],
                                              self.China_it_top100_dict)
                    # 判断是不是中国私营企业500强
                    self.get_company_type_num(article_title,
                                              self.China_private_top500_result[university_table_name],
                                              self.China_private_top500_dict)

                except BaseException as e:
                    print("Error===================================================")
                    print(e)
                    print(company)
                    print("Error===================================================")

    # 根据传入的标题和公司正规名称，判断标题中是否包含公司名称，结果存储在result_list中
    def get_company_type_num(self, article_title, result_list, company_short_names_list):
        # result_dict[university_table_name] = []
        for short_names in company_short_names_list:
            for short_name in short_names['short_name']:
                if article_title.find(short_name) != -1:
                    if 'wrong_name' in short_names:
                        for index, wrong_name in enumerate(short_names['wrong_name']):
                            # 表示在标题中找到了wrong_name，如
                            # 京东方科技集团股份有限公司近期到我校招聘
                            # short_name为京东， wrong_name为京东方
                            # 则此时不应该进行append， 立即退出这一层循环
                            if article_title.find(wrong_name) != -1:
                                # print(company+"：" + short_name + "-wrong name:" + wrong_name)
                                break
                            if article_title.find(wrong_name) == -1 and index == (len(short_names['wrong_name']) - 1):
                                result_list.append(short_name + "-->" + article_title)
                        # 为避免重复判断，及时跳出循环
                        break
                    else:
                        # 为避免重复判断，及时跳出循环
                        # print(short_name + "-->" + company)
                        result_list.append(short_name + "-->" + article_title)
                        break

    # 获取大学的列表
    def get_university_list(self):
        return self.re.lrange("university", 0, -1)

    def get_total_info(self):
        university_list = self.get_university_list()
        count = 0
        for name in university_list:
            count += self.re.llen(name)
        print(count)
        return count

    # 从文件中读取企业名单
    def get_company_short_name(self):
        with open("../data/ana_company_data/China_Top_500.json", 'r', encoding='utf-8') as r:
            self.China_top500_dict = json.load(r)
        with open("../data/ana_company_data/USA_Top_500.json", 'r', encoding='utf-8') as r:
            self.usa_top500_dict = json.load(r)
        with open("../data/ana_company_data/World_Top_500.json", 'r', encoding='utf-8') as r:
            self.world_top500_dict = json.load(r)
        with open("../data/ana_company_data/China_manufacture_company_top500.json", 'r', encoding='utf-8') as r:
            self.manufacture_top500_dict = json.load(r)
        with open("../data/ana_company_data/China_it_top_100_company_info.json", 'r', encoding='utf-8') as r:
            self.China_it_top100_dict = json.load(r)
        with open("../data/ana_company_data/China_service_company_top100.json", 'r', encoding='utf-8') as r:
            self.China_service_top100_dict = json.load(r)
        with open("../data/ana_company_data/China_private_company_top500.json", 'r', encoding='utf-8') as r:
            self.China_private_top500_dict = json.load(r)
        with open("../data/ana_company_data/investment_top100.json", 'r', encoding='utf-8') as r:
            self.world_investment_top100_dict = json.load(r)
        with open("../data/ana_company_data/best_consulting_company_info.json", 'r', encoding='utf-8') as r:
            self.world_consult_top75_dict = json.load(r)
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
                util.format_err(e, university_table_name, item)
                continue
        print("Finish to find 2017 Recruitment-->" + university_table_name)
        self.count += 1
        print(self.count)
        return company_list_2017, len(company_list_2017)

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
                util.format_err(e, item)
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
        waste_words = COMPANY_WASTE_WORDS
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
        return short_names

    # 保存到文件
    def add_to_file(self, file_name):
        # for py3
        with open(file_name + '.json', 'w', encoding='utf-8') as w:
            json.dump(self.data_array, w, ensure_ascii=False)
        self.data_array = []

    # 打印数据以及保存最终数据到文件
    def print_and_save_result(self, result_dict, filename):
        self.data_array = []
        for key, values in result_dict.items():
            print('--------------------------------------')
            print(key + ":" + str(len(values)) + " ".join(values))
            university_short_name = key[:-len('_company_info')]
            try:
                print(UNIVERSITY_INFO[university_short_name][0] + ":" + str(len(values)))
                self.data_array.append(dict(name=UNIVERSITY_INFO[university_short_name], data=values,
                                            total_num=self.university_company_list_length_dict[key]))
            except BaseException as e:
                util.format_err(e)
                continue
        with open('../data/result_data/' + filename + '.js', 'w', encoding='utf-8') as w:
            # json.dump(self.data_array, w, ensure_ascii=False)
            # 将json 数据转化为js的const 变量
            data_str = str(self.data_array).replace('\'', "\"")
            w.write("const " + filename + "=" + data_str)

#
# def test_get_university_company_list():
#     analysis = SmartAnalysisByName()
#     analysis.get_company_short_name()
#     university = analysis.get_university_list()
#     analysis.get_total_info()
#     analysis.get_univeristy_company_list(university_list=university)
#     print("到这些学校招聘的世界五百强================================")
#     analysis.print_and_save_result(analysis.world_top500_result, 'world_top500_result')
#     print("到这些学校招聘的中国五百强================================")
#     analysis.print_and_save_result(analysis.China_top500_result, 'China_top500_result')
#     print("到这些学校招聘的世界五百强================================")
#     analysis.print_and_save_result(analysis.usa_top500_result, 'usa_top500_result')
#     print("到这些学校招聘的中国IT业100强================================")
#     analysis.print_and_save_result(analysis.China_it_top100_result, 'China_it_top100_result')
#     print("到这些学校招聘的制造业500强================================")
#     analysis.print_and_save_result(analysis.China_manufacture_top500_result, 'China_manufacture_top500_result')
#     print("到这些学校招聘的私有企业500强================================")
#     analysis.print_and_save_result(analysis.China_private_top500_result, 'China_private_top500_result')
#     print("到这些学校招聘的服务业100强================================")
#     analysis.print_and_save_result(analysis.China_service_top100_result, 'China_service_top100_result')
#     print("到这些学校招聘的投资机构100强================================")
#     analysis.print_and_save_result(analysis.world_investment_top100_result, 'world_investment_top100_result')
#     print("到这些学校招聘的世界咨询业75强================================")
#     analysis.print_and_save_result(analysis.world_consult_top75_result, 'world_consult_top75_result')


# def test_get_real_name():
#     analysis = SmartAnalysisByName()
#     analysis.get_top_500_list()
#     analysis.get_top_500_real_name()
#
#
# def test_get_activity_degree():
#     pass


if __name__ == '__main__':
    # test_get_university_company_list()
    analysis = SmartAnalysisByName()
    analysis.get_company_short_name()
    university = analysis.get_university_list()
    analysis.get_total_info()
    analysis.get_univeristy_company_list(university_list=university)
    print("到这些学校招聘的世界五百强================================")
    analysis.print_and_save_result(analysis.world_top500_result, 'world_top500_result')
    print("到这些学校招聘的中国五百强================================")
    analysis.print_and_save_result(analysis.China_top500_result, 'China_top500_result')
    print("到这些学校招聘的世界五百强================================")
    analysis.print_and_save_result(analysis.usa_top500_result, 'usa_top500_result')
    print("到这些学校招聘的中国IT业100强================================")
    analysis.print_and_save_result(analysis.China_it_top100_result, 'China_it_top100_result')
    print("到这些学校招聘的制造业500强================================")
    analysis.print_and_save_result(analysis.China_manufacture_top500_result, 'China_manufacture_top500_result')
    print("到这些学校招聘的私有企业500强================================")
    analysis.print_and_save_result(analysis.China_private_top500_result, 'China_private_top500_result')
    print("到这些学校招聘的服务业100强================================")
    analysis.print_and_save_result(analysis.China_service_top100_result, 'China_service_top100_result')
    print("到这些学校招聘的投资机构100强================================")
    analysis.print_and_save_result(analysis.world_investment_top100_result, 'world_investment_top100_result')
    print("到这些学校招聘的世界咨询业75强================================")
    analysis.print_and_save_result(analysis.world_consult_top75_result, 'world_consult_top75_result')
    print("Finish")

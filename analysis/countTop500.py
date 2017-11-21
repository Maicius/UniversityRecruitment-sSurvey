import json

from jedis import jedis
import jieba


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

        self.usa_company_str = " ".join(self.USA_company_list)
        self.china_company_str = " ".join(self.China_company_list)
        self.world_company_str = " ".join(self.World_company_list)

    def get_university_top_500(self, university):
        university_list = self.re.lrange(university, 0, -1)
        self.get_top_500_list()
        self.get_university_company_name(university_list)

    def get_university_company_name(self, university_list):
        for university in university_list:
            self.china_top500_dict[university] = []
            self.world_top500_dict[university] = []
            self.usa_top500_dict[university] = []
            real_name_list = self.get_company_short_name(university)
            for name in real_name_list:
                if self.china_company_str.find(name) != -1:
                    self.china_top500_dict[university].append(name)
                if self.world_company_str.find(name) != -1:
                    self.world_top500_dict[university].append(name)
                if self.usa_company_str.find(name) != -1:
                    self.usa_top500_dict[university].append(name)
        print(self.china_top500_dict)

    # 获取到大学招聘的公司的真名
    def get_company_short_name(self, university):
        company_list = self.re.lrange(university, 0, -1)
        real_name_list = []
        province = ['北京', '上海', '天津', '重庆', '云南', '西藏', '新疆','广西', '内蒙古', '湖南','湖北', '广东', '贵州', '河北', '黑龙江', '沈阳', '辽宁']
        for company in company_list:
            try:
                company = company.replace('\'', '"')
                company = json.loads(company)
                company_name = company['company_name']
                real_name = self.get_jieba_fenci(company_name)
                if real_name != '' and real_name != '(' and real_name != '）' and real_name not in province:
                    real_name_list.append(real_name)
                # print(real_name)
            except BaseException as e:
                print("error=============================================================")
                print(company)
                print(e)
                print("error=============================================================")
                continue
        return real_name_list

    # 根据标题内容截取公司的真名
    def get_jieba_fenci(self, company_name):
        waste_words = ['碧', '股票代码', '600180', '宣讲会', '招聘会', '招聘', '正式启动', '实习', '校园', '实习生', '管培生', '选调生', '已更改',
                       '春季', '秋季', '届', '级', '部门','集团', '公司', '有限', '事务所', '资本', '？', '研究院', '研究所', '有限公司', '股份有限公司'
                       '蜂', '起', '云涌', '名企', '面向', '应届', '毕业生', '...', '专场', '年', '面试', '及', '启事', '招聘启事', '上', '双选会',
                       '人才','取消', '·', '梦想校园行',
                       '引进', '推介会', '暑期', '冬季', '公告', '引进人才', '互娱'
                       '已来', '不来' '与你共创未来！' '与你', '共创', '计划', '“', '无界', '”', '近期', '【','】', '，']
        years = ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011','(', '（', '18', '17', '16', '15', '14', '13' '12', '11']
        title = ['公司', '集团', '务所', '学校', '大学', '中学', '小学', '究院', '资本', '银行', '航空', '工业']

        city = ['上海', '北京']
        single = ['-', '——', '—']
        double = ['--']
        print("===============")
        print(company_name + ":")

        if company_name.find('已举办') != -1:
            company_name = company_name[5:]
        if company_name.find('举办') != -1:
            company_name = company_name[4:]

        # 对于文字出现了title中词组的标题
        # 对于学校要考虑是否为附属中学等
        for item in title:
            index = company_name.find(item)
            if (index + 2) < len(company_name):
                if index != -1 and company_name[index + 2] != '附' and company_name[index + 2] != '工' and company_name[index + 2] != '和':
                    company_name = company_name[:index + 2]

        # 对于文字中出现了年度等字样的标题
        # 如 苏州新区高新技术产业2017校园招聘宣讲会
        # 特殊情况为年份在标题开头
        # 如 2017新疆自治区人才引进计划宣讲会
        for item in years:
            index = company_name.find(item)
            if index != -1 and index != 0:
                company_name = company_name[:index]
            elif index == 0:
                company_name = company_name[4:]

        # 对于出现了破折号等特殊符号的情况
        # 同时去掉一汽-大众这个特殊情况
        for item in single:
            index = company_name.find(item)
            if index != -1 and company_name.find('一汽-大众') == -1:
                company_name = company_name[index + 1:]

        for item in city:
            index = company_name.find(item)
            if index != -1 and index != 0:
                company_name = company_name[index:]
        # 这个公司名称实在太特殊了
        if company_name.find('俺来也') != -1:
            real_name = company_name
        # 根据词料库去掉无意义文字
        else:
            short_names = jieba.cut(company_name, cut_all=False)
            word_list = []
            for item in short_names:
                if "".join(waste_words).find(item) == -1:
                    word_list.append(item)
            real_name = "".join(word_list).strip()
        print(real_name)
        return real_name

    def test_fenci(self):
        test_words = []
        # test_words.append("苏州新区高新技术产业股份有限公司2017校园招聘宣讲会")
        # test_words.append("苏州新区高新技术产业股份有限公司数据中心2017校园招聘宣讲会")
        # test_words.append("苏州新区高新技术产业2017校园招聘宣讲会")
        # test_words.append("安永华明会计师事务所（特殊普通...")
        # test_words.append("中国银行股份有限公司上海市分行")
        # test_words.append("上海交通大学就业中心")
        # test_words.append("摩根士丹利2018宣讲会")
        test_words.append("我的世界我的世界——摩根士丹利2018宣讲会")
        test_words.append("“Hi澳海，High未来”——澳海控股2018校园招聘启动啦!")
        test_words.append("“未来 无界”第一资产2018届校园招聘宣讲会")
        test_words.append("未来已来，你来不来！微分与你共创未来！")
        test_words.append("2017新疆自治区人才引进计划宣讲会")
        test_words.append("一汽-大众2017宣讲会")
        test_words.append("俺来也2017管培生计划全国校园招聘会")
        test_words.append("美好世界，由你开启 - ABB2018校园招聘")
        test_words.append("西北工业大学附属中学2018招聘会")
        test_words.append("[已举办]广东惠州市仲恺高新区事业单位2014校园宣讲招聘会:")
        test_words.append("[举办]2017广东惠州市仲恺高新区事业单位2014校园宣讲招聘会")
        test_words.append("一起见证时光的奇迹上海禾赛光电")
        test_words.append("凯泰资本欢迎加入我们创业者一起改变世界")
        test_words.append("中国工程物理研究院招生暨相约中物院 实践强国梦夏令营宣传")
        test_words.append("中国航空工业集团公司招聘双选会")
        test_words.append("中国直升机设计研究所-中航工业602宣讲会")
        test_words.append("从能源角度看中国移动交通的未来-壳牌招聘")
        test_words.append("[已举办]航空工业沈阳飞机设计研究所（601所） 2018届高校毕业生招聘信息")
        test_words.append("杭州品茗股份18年校园招聘-百人计划")
        test_words.append("工业和信息化部人才交流中心（2017年度）全国硕博专场秋季巡回招聘会")
        test_words.append("腾讯互娱 · 梦想校园行")
        test_words.append("华为2018届北京地区校园招聘启动")
        test_words.append("华为公司岗位推介（制造专场）")
        for item in test_words:
            self.get_jieba_fenci(item)


if __name__ == '__main__':
    analysis = AnalysisTop500()
    # analysis.get_top_500_list()
    # analysis.get_university_top_500("university")
    analysis.test_fenci()

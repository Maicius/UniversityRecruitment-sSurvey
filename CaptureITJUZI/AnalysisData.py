import json
import xlwt

from Util import Util


def get_raw_data():
    re = Util.jedis().get_re()
    company_list = []
    temp = re.lrange("intelli_drive", 0, -1)
    company_list.append(temp)
    temp = re.lrange("car_net", 0, -1)
    company_list.append(temp)
    temp = re.lrange("driving_without_man", 0, -1)
    company_list.append(temp)
    temp = re.lrange("intelli_car", 0, -1)
    company_list.append(temp)
    return company_list


def do_analysis(company_list):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet("worksheet")
    row0 = ['公司名称', '细分行业', '融资时间', '融资轮次', '融资金额', '投资人']
    save_row(worksheet, row0, 0)
    col = 1
    for k in range(0, len(company_list)):
        print(k)
        companys = company_list[k]
        for com in companys:
            # print(com)
            print(col)
            com = json.loads(com.replace("'", "\""))
            company_name = com['company_name']
            industry = com['industry']
            if com['financing'] != '':
                people = ",".join(com['people'])
                financing_times = len(com['financing'])
                data = com['financing']
                for i in range(financing_times):
                    time = data[i]['融资时间']
                    mount = data[i]['融资金额']
                    row = [company_name, industry, time, i + 1, mount, people]
                    save_row(worksheet, row, col)
                    col += 1
                    workbook.save("报表.xls")
            else:
                financing_times = 0
                time = ""
                mount = ""
                people = ""
                row = [company_name, industry, time, financing_times, mount, people]
                save_row(worksheet, row, col)
                col += 1
                workbook.save("报表.xls")

    workbook.save("报表.xls")


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


def save_row(worksheet, row, col):
    for i in range(0, len(row)):
        print(row[i])
        worksheet.write(col, i, row[i])


if __name__ == "__main__":
    company_list = get_raw_data()
    print(len(company_list[1]))
    do_analysis(company_list)

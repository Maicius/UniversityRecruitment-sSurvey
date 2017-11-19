# coding = utf-8
import json


def analysis(filename):
    with open(filename, 'r', encoding="utf-8") as w:
        data = json.load(w)
    for i in range(len(data)):
        com_name = data[i]
        print(str(com_name))
        company_name = com_name['company_name']
        date = data[i]['date']
        print(company_name + date)

    for item in data:
        company_name = item['company_name']

    print(len(data))

if __name__ == '__main__':
    analysis('/Users/maicius/code/UniversityRecruitmentSurvey/data/CSU_company_info.json')
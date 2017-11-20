# coding = utf-8
import json


def analysis(filename):
    dateDict = {}
    dateList = []
    dateList.append(1)
    with open(filename, 'r', encoding="utf-8") as w:
        data = json.load(w)
    for i in range(len(data)):
        com_name = data[i]
        print(str(com_name))
        company_name = com_name['company_name']
        # date = data[i]['date']
        if data[i]['date']in dateDict:
            dateDict[data[i]['date']] += 1
        else:
            dateDict[data[i]['date']] = 1
        print(company_name + data[i]['date'])

    print(dateDict['2017-12-03'])
    # for item in data:
    #     company_name = item['company_name']
    print(dateDict.values())
    print(dateDict.keys())
    print(dateDict.get(0))

if __name__ == '__main__':
    analysis('/Users/maicius/code/UniversityRecruitmentSurvey/data/CSU_company_info.json')
from analysis.SmartAnalysisByName import SmartAnalysisByName


class SmartAnalysisByDate(object):
    def __init__(self):
        analysis_by_name = SmartAnalysisByName()
        self.all_company_date_list = []
        self.university_list = analysis_by_name.get_university_list()


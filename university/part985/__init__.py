from university.main.Recruitment import Recruitment
from university.part985.CQURescruitment import get_cqu_recruit
from university.part985.CSURecruitment import get_csu_recruit
from university.part985.HUSTRecruitment import get_hust_recruit
from university.part985.LZURecruitment import get_lzu_rescruit
from university.part985.UESTCRecruitment import get_uestc_recruit


def get_985_infos():
    recruit = Recruitment()
    recruit.get_sjtu_rescruit()
    get_cqu_recruit()
    get_csu_recruit()
    get_hust_recruit()
    get_lzu_rescruit()
    get_uestc_recruit()

if __name__ == '__main__':
    get_985_infos()
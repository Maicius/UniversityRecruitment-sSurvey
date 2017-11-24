from university.main.Recruitment import Recruitment
from university.part985.CQURescruitment import get_cqu_recruit
from university.part985.CSURecruitment import get_csu_recruit
from university.part985.HUSTRecruitment import get_hust_recruit
from university.part985.LZURecruitment import get_lzu_rescruit
from university.part985.NKURecruitment import get_nku_recruit
from university.part985.UESTCRecruitment import get_uestc_recruit
from util import util


def get_985_infos():
    try:
        recruit = Recruitment()
        recruit.get_sjtu_rescruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_csu_recruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_cqu_recruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_hust_recruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_lzu_rescruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_uestc_recruit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_nku_recruit()
    except BaseException as e:
        util.format_err(e)
        pass

if __name__ == '__main__':
    get_985_infos()
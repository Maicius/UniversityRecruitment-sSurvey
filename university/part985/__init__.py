from university.main.Recruitment import Recruitment
from university.part985.BHURecruitment import get_bhu_recruitment
from university.part985.CQURescruitment import get_cqu_recruit
from university.part985.CSURecruitment import get_csu_recruit
from university.part985.HUSTRecruitment import get_hust_recruit
from university.part985.JLURecruitment import get_jlu_recruitment
from university.part985.LZURecruitment import get_lzu_rescruit
from university.part985.NKURecruitment import get_nku_recruit
from university.part985.NWAFURecruitment import get_nwafu_recruitment
from university.part985.OUCRecruitment import get_ouc_recruit
from university.part985.SCUTRecruitment import get_scut_recuit
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
    try:
        get_scut_recuit()
    except BaseException as e:
        util.format_err(e)
        pass
    try:
        get_ouc_recruit()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_bhu_recruitment()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_jlu_recruitment()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_nwafu_recruitment()
    except BaseException as e:
        util.format_err(e)
        pass
if __name__ == '__main__':
    get_985_infos()
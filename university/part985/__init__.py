from university.main.Recruitment import Recruitment
from university.part985.BHURecruitment import get_bhu_recruitment
from university.part985.BNURecruitment import get_bnu_recuit
from university.part985.CAURecruitment import get_cau_recruitment
from university.part985.CQURescruitment import get_cqu_recruit
from university.part985.CSURecruitment import get_csu_recruit
from university.part985.DLUTRecruitment import get_dlut_recruitment
from university.part985.ECNURecruitment import get_ecnu_recruitment
from university.part985.HNURecruitment import get_hnu_recuit
from university.part985.HUSTRecruitment import get_hust_recruit
from university.part985.JLURecruitment import get_jlu_recruitment
from university.part985.LZURecruitment import get_lzu_rescruit
from university.part985.MUCRecruitment import get_muc_recuitment
from university.part985.NKURecruitment import get_nku_recruit
from university.part985.NWAFURecruitment import get_nwafu_recruitment
from university.part985.OUCRecruitment import get_ouc_recruit
from university.part985.RUCRecruitment import get_ruc_recruitment
from university.part985.SCURecruitment import get_scu_recruit
from university.part985.SCUTRecruitment import get_scut_recuit
from university.part985.TJURecuitment import get_tju_recruitment
from university.part985.UESTCRecruitment import get_uestc_recruit
from util import util


def get_985_infos():
    try:
        get_scu_recruit()
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

    try:
        get_hnu_recuit()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_muc_recuitment()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_dlut_recruitment()
    except BaseException as e:
        util.format_err(e)
        pass

    try:
        get_bnu_recuit()
    except BaseException as e:
        util.format_err(e)

    try:
        get_ecnu_recruitment()
    except BaseException as e:
        util.format_err(e)

    try:
        get_tju_recruitment()
    except BaseException as e:
        util.format_err(e)

    try:
        get_cau_recruitment()
    except BaseException as e:
        util.format_err(e)

    try:
        get_ruc_recruitment()
    except BaseException as e:
        util.format_err(e)
if __name__ == '__main__':
    get_985_infos()
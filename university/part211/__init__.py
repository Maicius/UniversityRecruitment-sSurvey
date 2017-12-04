from university.part211.CAURecruitment import get_cau_recruitment
from university.part211.CUFERescruitment import get_cufe_rescruit
from university.part211.GZURecruitment import get_gzu_recruit
from university.part211.HNURecruitment import get_hnu_recruitment
from university.part211.LMURecruitment import get_lmu_recruitment
from university.part211.LNURecruitment import get_lnu_recruitment
from university.part211.SHZURecruitment import get_shzu_recruitment
from university.part211.SUFERescruitment import get_sufe_recruit
from university.part211.SWURecruitment import get_swu_recruitment
from university.part211.USTBRecruitment import get_ustbr_recuitment
from university.part211.ZZURecruitment import get_zzu_recruit
from util import util


# 获取所有211的数据
def get_211_infos():
    try:
        get_cufe_rescruit()
    except BaseException as e:
        util.format_err(e, "cufe")
        pass
    try:
        get_sufe_recruit()
    except BaseException as e:
        util.format_err(e, "sufe")
        pass
    try:
        get_ustbr_recuitment()
    except BaseException as e:
        util.format_err(e, "ustb")
        pass

    try:
        get_swu_recruitment()
    except BaseException as e:
        util.format_err(e, "swu")
        pass

    try:
        get_zzu_recruit()
    except BaseException as e:
        util.format_err(e, "zzu")
        pass

    try:
        get_shzu_recruitment()
    except BaseException as e:
        util.format_err(e, "shzu")
        pass
    try:
        get_gzu_recruit()
    except BaseException as e:
        util.format_err(e, "gzu")
        pass

    try:
        get_hnu_recruitment()
    except BaseException as e:
        util.format_err(e, "gzu")
        pass

    try:
        get_cau_recruitment()
    except BaseException as e:
        util.format_err(e, "cnu")
        pass

    try:
        get_lmu_recruitment()
    except BaseException as e:
        util.format_err(e, "lmu")
        pass

    try:
        get_lnu_recruitment()
    except BaseException as e:
        util.format_err(e, "lmu")
        pass

    util.format_err("获取211数据完成")

if __name__ == '__main__':
    get_211_infos()
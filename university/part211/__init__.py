from university.part211.CUFERescruitment import get_cufe_rescruit
from university.part211.SUFERescruitment import get_sufe_recruit
from university.part211.USTBRecruitment import get_ustbr_recuitment
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
        util.format_err(e, "ustbr")
        pass

    util.format_err("获取211数据完成")

if __name__ == '__main__':
    get_211_infos()
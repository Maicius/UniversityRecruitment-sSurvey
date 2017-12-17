from university.c9.FDURescruitment import get_fdu_rescruit
from university.c9.NJURescruitment import get_nju_rescruit
from university.c9.THURecruitment import get_tsinghua_recruit
from university.c9.USTCRecruitment import get_ustc_recruit
from university.c9.XJTURecruitment import get_XJTU_recruit
from university.main.Recruitment import Recruitment
from university.c9.PKURecruitment import get_pku_recruit
from university.c9.HITRescruitment import get_hit_rescruit
from university.c9.ZJURescruitment import get_zju_rescruit
from util import util


# 获取C9 所有学校的招聘数据
def get_c9_info():
    print("Begin to collect c9's information")
    try:
        recruit = Recruitment()
        recruit.get_sjtu_rescruit()
    except BaseException as e:
        util.format_err(e, "sjtu")
        pass

    try:
        get_tsinghua_recruit()
    except BaseException as e:
        util.format_err(e, "thu")
        pass

    try:
        get_fdu_rescruit()
    except BaseException as e:
        util.format_err(e, "fdu")
        pass

    try:
        get_ustc_recruit()
    except BaseException as e:
        util.format_err(e, "ustc")
        pass
    try:
        get_hit_rescruit()
    except BaseException as e:
        util.format_err(e, "hit")
        pass
    try:
        get_zju_rescruit()
    except BaseException as e:
        util.format_err(e, "zju")
        pass
    try:
        get_XJTU_recruit()
    except BaseException as e:
        util.format_err(e, "xjtu")
        pass

    try:
        get_nju_rescruit()
    except BaseException as e:
        util.format_err(e, "nju")
        pass

    try:
        # 北大的需要更新cookie
        get_pku_recruit()
    except BaseException as e:
        util.format_err(e, "pku")
        pass


if __name__ == "__main__":
    get_c9_info()

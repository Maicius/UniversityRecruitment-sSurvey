from university.top_public.CUEBRecruitment import get_cueb_recuitment
from university.top_public.HBURecruitment import get_hbu_recruitment
from university.top_public.HQURecruitment import get_hqu_recruitment
from university.top_public.HZNURecruitment import get_hznu_recruitment
from university.top_public.NCEPURecruitment import get_ncepu_recruit
from university.top_public.NCUTRecruitment import get_ncut_recuitment
from university.top_public.NJUPTRecruitment import get_njupt_recruitment
from university.top_public.WUSTRecruitment import get_wust_recruitment
from university.top_public.YSURecruitment import get_ysu_recruitment
from util import util


def get_top_public_infos():
    print("开始获取一本数据=====================")
    try:
        get_ncepu_recruit()
    except BaseException as e:
        util.format_err(e, "ncepu")
        pass
    try:
        get_ncut_recuitment()
    except BaseException as e:
        util.format_err(e, "ncut")
        pass
    try:
        get_njupt_recruitment()
    except BaseException as e:
        util.format_err(e, "njupt")
        pass
    try:
        get_ysu_recruitment()
    except BaseException as e:
        util.format_err(e, "ysu")
        pass
    try:
        get_hqu_recruitment()
    except BaseException as e:
        util.format_err(e, "hqu")
        pass
    try:
        get_hznu_recruitment()
    except BaseException as e:
        util.format_err(e, "hznu")
        pass

    try:
        get_cueb_recuitment()
    except BaseException as e:
        util.format_err(e, "hznu")
        pass

    try:
        get_wust_recruitment()
    except BaseException as e:
        util.format_err(e, "hznu")
        pass
    try:
        get_hbu_recruitment()
    except BaseException as e:
        util.format_err(e, "hznu")
        pass

    print("获取一本数据完成=====================")

if __name__ == '__main__':
    get_top_public_infos()
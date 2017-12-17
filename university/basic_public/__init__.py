from university.basic_public.BIPTRecruitment import get_bipt_recruitment
from university.basic_public.CUITRecruitment import get_cuit_recruit
from university.basic_public.JHURecruitment import get_jhu_recruitment
from university.basic_public.JCXYRecruitment import get_jincheng_recruit
from university.basic_public.LUTRecruitment import get_lut_recruitment
from university.basic_public.SCCRecruitment import get_scc_recuit
from university.basic_public.TJPURecruitment import get_tjpu_recruitment
from university.basic_public.WZURecruitment import get_wzu_recruitment
from university.basic_public.YANGTZEURecruitment import get_yangtzeu_recruitment
from university.basic_public.YTURecruitment import get_ytu_recruitment
from util import util


def get_basic_public_info():
    try:
        get_bipt_recruitment()
    except BaseException as e:
        util.format_err(e, "bipt")
        pass

    try:
        get_cuit_recruit()
    except BaseException as e:
        util.format_err(e, "cuit")
        pass

    try:
        get_jhu_recruitment()
    except BaseException as e:
        util.format_err(e, "jhu")
        pass

    try:
        get_jincheng_recruit()
    except BaseException as e:
        util.format_err(e, "jcxy")
        pass

    try:
        get_scc_recuit()
    except BaseException as e:
        util.format_err(e, "scc")
        pass

    try:
        get_tjpu_recruitment()
    except BaseException as e:
        util.format_err(e, "tjpu")
        pass

    try:
        get_wzu_recruitment()
    except BaseException as e:
        util.format_err(e, "wzu")
        pass

    try:
        get_ytu_recruitment()
    except BaseException as e:
        util.format_err(e, "ytu")
        pass

    try:
        get_yangtzeu_recruitment()
    except BaseException as e:
        util.format_err(e, "yangtzeu")
        pass

    try:
        get_lut_recruitment()
    except BaseException as e:
        util.format_err(e, "yangtzeu")
        pass


if __name__ == '__main__':
    get_basic_public_info()

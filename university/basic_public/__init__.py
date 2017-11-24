from university.basic_public.BIPTRecruitment import get_bipt_recruitment
from university.basic_public.CUITRecruitment import get_cuit_recruit
from university.basic_public.JHURecruitment import get_jhu_recruitment
from university.basic_public.JCXYRecruitment import get_jincheng_recruit
from university.basic_public.SCCRecruitment import get_scc_recuit
from university.basic_public.TJPURecruitment import get_tjpu_recruitment
from university.basic_public.WZURecruitment import get_wzu_recruitment
from university.basic_public.YTURecruitment import get_ytu_recruitment


def get_basic_public_info():
    get_bipt_recruitment()
    get_cuit_recruit()
    get_jhu_recruitment()
    get_jincheng_recruit()
    get_scc_recuit()
    get_tjpu_recruitment()
    get_wzu_recruitment()
    get_ytu_recruitment()

if __name__ == '__main__':
    get_basic_public_info()
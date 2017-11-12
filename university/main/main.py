from university.basic_public.JinChengRecruitment import get_jincheng_recruit
from university.c9.FDURescruitment import get_fdu_rescruit
from university.c9.NJURescruitment import get_nju_rescruit
from university.c9.TsingHuaRecruitment import get_tsinghua_recruit
from university.main.Recruitment import Recruitment
from university.part211.CUFERescruitment import get_cufe_rescruit
from university.part211.SUFERescruitment import get_sufe_recruit
from university.part985.CQURescruitment import get_cqu_recruit
from university.part985.HUSTRecruitment import get_hust_recruit
from university.part985.LZURecruitment import get_lzu_rescruit
from university.part985.UESTCRecruitment import get_uestc_recruit


if __name__ == '__main__':
    print("Begin to collect all infomation")
    # 上海交通大学与四川大学的就业网是一个模板
    recruit = Recruitment()
    recruit.get_scu_recruit()
    recruit.get_sjtu_rescruit()
    get_tsinghua_recruit()
    get_jincheng_recruit()
    get_nju_rescruit()
    get_cufe_rescruit()
    get_lzu_rescruit()
    get_uestc_recruit()
    get_sufe_recruit()
    get_fdu_rescruit()
    get_cqu_recruit()
    get_hust_recruit()
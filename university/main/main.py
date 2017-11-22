from university.basic_public.JinChengRecruitment import get_jincheng_recruit
from university.c9 import get_c9_info
from university.c9.FDURescruitment import get_fdu_rescruit
from university.c9.NJURescruitment import get_nju_rescruit
from university.c9.THURecruitment import get_tsinghua_recruit
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
    get_c9_info()
from university.c9.FDURescruitment import get_fdu_rescruit
from university.c9.NJURescruitment import get_nju_rescruit
from university.c9.THURecruitment import get_tsinghua_recruit
from university.c9.USTCRecruitment import get_ustc_recruit
from university.c9.XJTURecruitment import get_XJTU_recruit
from university.main.Recruitment import Recruitment
from university.c9.PKURecruitment import get_pku_recruit
from university.c9.HITRescruitment import get_hit_rescruit
from university.c9.ZJURescruitment import get_zju_rescruit


# 获取C9 所有学校的招聘数据
def get_c9_info():
    print("Begin to collect c9's information")
    recruit = Recruitment()
    recruit.get_sjtu_rescruit()
    get_tsinghua_recruit()
    get_fdu_rescruit()
    get_ustc_recruit()
    get_hit_rescruit()
    get_zju_rescruit()
    get_XJTU_recruit()
    get_nju_rescruit()
    # 北大的需要更新cookie
    get_pku_recruit()

if __name__ == "__main__":
    get_c9_info()
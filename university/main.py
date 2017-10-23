from university.CUFERescruitment import get_cufe_rescruit
from university.JinChengRecruitment import get_jincheng_recruit
from university.LZURecruitment import get_lzu_rescruit
from university.NJURescruitment import get_nju_rescruit
from university.Recruitment import Recruitment
from university.TsingHuaRecruitment import get_tsinghua_recruit


if __name__ == '__main__':
    # 上海交通大学与四川大学的就业网是一个模板
    recruit = Recruitment()
    recruit.get_scu_recruit()
    recruit.get_sjtu_rescruit()
    get_tsinghua_recruit()
    get_jincheng_recruit()
    get_nju_rescruit()
    get_cufe_rescruit()
    get_lzu_rescruit()
from university.part211.CUFERescruitment import get_cufe_rescruit
from university.part211.SUFERescruitment import get_sufe_recruit
from university.part211.USTBRecruitment import get_ustbr_recuitment


def get_211_infos():
    get_cufe_rescruit()
    get_sufe_recruit()
    get_ustbr_recuitment()

if __name__ == '__main__':
    get_211_infos()
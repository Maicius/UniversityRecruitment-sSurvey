from university.basic_public import get_basic_public_info
from university.c9 import get_c9_info
from university.part211 import get_211_infos
from university.part985 import get_985_infos
from university.top_public import get_top_public_infos

if __name__ == '__main__':
    print("Begin to collect all information")
    get_c9_info()
    get_basic_public_info()
    get_985_infos()
    get_211_infos()
    get_top_public_infos()
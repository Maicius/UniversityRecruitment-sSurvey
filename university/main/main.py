from university.basic_public import get_basic_public_info
from university.c9 import get_c9_info
from university.part985 import get_985_infos

if __name__ == '__main__':
    print("Begin to collect all infomation")
    get_c9_info()
    get_basic_public_info()
    get_985_infos()
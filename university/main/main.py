import multiprocessing

from university.basic_public import get_basic_public_info
from university.c9 import get_c9_info
from university.part211 import get_211_infos
from university.part985 import get_985_infos
from university.top_public import get_top_public_infos
import logging
if __name__ == '__main__':
    print("Begin to collect all information")
    c9 = multiprocessing.Process(target=get_c9_info)
    c9.daemon = True
    p985 = multiprocessing.Process(target=get_985_infos)
    p985.daemon = True
    p211 = multiprocessing.Process(target=get_211_infos)
    p211.daemon = True
    top = multiprocessing.Process(target=get_top_public_infos)
    top.daemon = True
    basic = multiprocessing.Process(target=get_basic_public_info)
    basic.daemon = True
    print("Init Logging System...")
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    print("C9 Process start on====================================")
    c9.start()
    print("985 Process start on====================================")
    p985.start()
    print("211 Process start on====================================")
    p211.start()
    print("一本 Process start on====================================")
    top.start()
    print("二本 Process start on====================================")
    basic.start()

    c9.join()
    p985.join()
    p211.join()
    top.join()
    basic.join()
# coding:UTF-8
from lib.logging_lib import log
<<<<<<< HEAD
import fetch.scau_scautiu
import fetch.scau_arts
import fetch.scau_slxy
import fetch.scau_gongguan
import fetch.scau_info
=======
import fetch.scau_souyi
import fetch.scau_yuanyi
import fetch.scau_zihuan
import fetch.scau_nongxue
import fetch.scau_gongcheng
>>>>>>> origin/banana
import traceback


def main():
    log.info("爬虫启动！")

    fetchs = []
<<<<<<< HEAD
    # 电子工程
    fetchs.append(fetch.scau_scautiu.init)
    # 艺术学院
    fetchs.append(fetch.scau_arts.init)
    # 水利学院
    fetchs.append(fetch.scau_slxy.init)
    # 公管学院
    fetchs.append(fetch.scau_gongguan.init)
    # 信息学院
    fetchs.append(fetch.scau_info.init)
=======
    # 农学院
    fetchs.append(fetch.scau_nongxue.init)
    print('='*30)
    # 园艺学院
    fetchs.append(fetch.scau_yuanyi.init)
    print('='*55)
    # 资环学院
    fetchs.append(fetch.scau_zihuan.init)
    print('=' * 55)
    # 兽医学院
    fetchs.append(fetch.scau_souyi.init)
    print('=' * 55)

    # 工程学院
    fetchs.append(fetch.scau_gongcheng.init)
    print('=' * 55)
>>>>>>> origin/banana

    for func in fetchs:
        try:
            func()
        except:
            traceback.print_exc()

    log.info("爬虫结束！")


if __name__ == '__main__':
    main()

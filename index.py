# coding:UTF-8


from lib.logging_lib import log
import fetch.scautiu
import fetch.arts
import traceback


def main():
    log.info("爬虫启动！")

    fetchs = []
    # 电子工程
    #fetchs.append(fetch.scautiu.init)
    # 艺术学院
    # fetchs.append(fetch.arts.init)

    for func in fetchs:
        try:
            func()
        except:
            traceback.print_exc()

    log.info("爬虫结束！")


if __name__ == '__main__':
    main()

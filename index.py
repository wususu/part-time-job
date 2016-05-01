# coding:UTF-8


from lib.logging_lib import log
import fetch.scaulife
import fetch.scaucaineng
import fetch.scaudongke
import fetch.scaulinxue
import fetch.scauspxy
import fetch.scaurw
import traceback


def main():
    log.info("爬虫启动！")

    fetchs = []
    # 生命科学学院
    # fetchs.append(fetch.scaulife.init)
    # 材料与能源学院
    # fetchs.append(fetch.scaucaineng.init)
    # 动科学院
    # fetchs.append(fetch.scaudongke.init)
    # 林学
    # fetchs.append(fetch.scaulinxue.init)
    # 食品学院
    # fetchs.append(fetch.scauspxy.init)
    #人文学院
    fetchs.append(fetch.scaurw.init)
    for func in fetchs:
        try:
            func()
        except:
            traceback.print_exc()

    log.info("爬虫结束！")


if __name__ == '__main__':
    main()

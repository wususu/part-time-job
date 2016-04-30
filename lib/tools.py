# coding:UTF-8


"""
常用工具类

"""


from bs4 import BeautifulSoup
import re
import time
import random


def handle_company_name_use_black_data(objs, index):
    """
    采用黑名单过滤数据
    :param c:
    :return:
    """
    for obj in objs:
        if re.search(r'([随着]|[成立]|[负责])+.*?([公司]|[企业]|[集团]|[公司]|[研发中心])+', obj[index]):
            continue
        return obj[index]

    return objs[0][index]


def get_company_name(html):
    """
    提取公司名字
    :param html: 一段字符串
    :return:
    """
    html = BeautifulSoup(html, "html.parser").get_text()
    r = re.findall(r'(.*\d+年{0,1}的)?(.*[：，,。]+)?(.*?有限公司)', html)

    if r:
        return handle_company_name_use_black_data(r, 2)

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?(.*?研发中心)', html)
    if r:
        return handle_company_name_use_black_data(r, 2)

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?是?(.*?集团)', html)
    if r:
        return handle_company_name_use_black_data(r, 2)

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?(.*?公司)', html)
    if r:
        return handle_company_name_use_black_data(r, 2)

    return "未识别的公司"


def get_work_citys(html):
    """
    获取工作城市
    :param html: 一段字符串
    :return:
    """
    html = BeautifulSoup(html, "html.parser").get_text()
    r = re.findall(r'(工作地[点]?[:：]?){1}(可选：)?(.*)', html)
    if r and r[0][2]:
        return re.split(r'[#,、，\s]', r[0][2])
    return []


def get_work_position(html):
    """
    获取职位
    :param html: 一段字符串
    :return:
    """
    return []


def get_real_time(time_str):
    """
    获取标准的时间
    :param time_str:
    :return:
    """
    time_str = time_str.replace('年', '-')
    time_str = time_str.replace('月', '-')
    time_str = time_str.replace('日', '')
    time_str = time_str.replace('时', '：')
    time_str = time_str.replace('分', '：')
    time_str = time_str.replace('秒', '')

    attrs = time_str.split(' ')
    t = attrs[0]
    if not t:
        t = attrs[1]

    arrs = t.split("-")
    if len(arrs) != 3:
        t = time.strftime("%Y-") + t

    return t + " 00:00:00"


def sleep_some_time():
    """
    随机休眠几秒
    :return:
    """
    t = random.random() / 2 * 10
    print("休眠" + str(t) + "秒")
    time.sleep(t)

# with open('../debug_html/2.html', 'r') as fp:
#     print(get_work_citys(fp.read()))

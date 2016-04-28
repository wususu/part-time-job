# coding:UTF-8


"""
常用工具类

"""


from bs4 import BeautifulSoup
import re


def get_company_name(html):
    """
    提取公司名字
    :param html: 一段字符串
    :return:
    """
    html = BeautifulSoup(html, "html.parser").get_text()
    r = re.findall(r'(.*\d+年{0,1}的)?(.*[：，,。]+)?(.*?有限公司)', html)

    if r:
        return r[0][2]

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?(.*?研发中心)', html)
    if r:
        return r[0][2]

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?(.*?集团)', html)
    if r:
        return r[0][2]

    r = re.findall(r'(.*\d+年?的)?(.*[：，,。]+)?(.*?公司)', html)
    if r:
        return r[0][2]

    return "未识别的公司"


def get_work_citys(html):
    """
    获取工作城市
    :param html: 一段字符串
    :return:
    """
    return []


def get_work_position(html):
    """
    获取职位
    :param html: 一段字符串
    :return:
    """
    return []


with open('../debug_html/2.html', 'r') as fp:
    print(get_company_name(fp.read()))

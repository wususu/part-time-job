# coding:UTF-8


"""
常用工具类

"""


from bs4 import BeautifulSoup
import re
import requests

def text_filter(text):
    filter_strs=["\xa0","\ufffd","\u200b","\u2022"]
    for filter_str in filter_strs:
        text=text.replace(filter_str,"")
    return text

def get_html(url):
    response = requests.get(url)
    return response.content

def get_html_t(url):
    response = requests.get(url)
    return response.text

def get_release_time(html):
    html = BeautifulSoup(html, "html.parser").get_text()
    r=re.findall(r"(\d{4}\-\d+\-\d+)",html)
    if r:
        return r[0]

    r=re.findall(r"(\d+\-\d+)发布",html)
    if r:
        return r[0]

def handle_company_name_use_black_data(objs, index):
    """
    采用黑名单过滤数据
    :param c:
    :return:
    """
    for obj in objs:
        if re.search(r'([随着]|[成立])+.*?([公司]|[企业]|[集团]|[公司]|[研发中心])+', obj[index]):
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


# with open('../debug_html/2.html', 'r') as fp:
#     print(get_work_citys(fp.read()))

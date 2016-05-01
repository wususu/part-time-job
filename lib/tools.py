# coding:UTF-8


"""
常用工具类

"""


from bs4 import BeautifulSoup
from config.citys import citys
from config.position import positions
import re
import time
import random
import requests

def text_filter(text):
    filter_strs=["\xa0","\ufffd","\u200b","\u2022"]
    for filter_str in filter_strs:
        text=text.replace(filter_str,"")
    return text

def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, response.status_code))
    return response.content

def get_html_t(url,coding="utf-8"):
    response = requests.get(url)
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, response.status_code))

    content=str(response.content)
    r=re.findall("charset=(\w+)\"",content)
    if r:
        coding=r[0].lower()
    response.encoding=coding
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
        if re.search(r'([随着]|[成立]|[负责])+.*?([公司]|[企业]|[集团]|[公司]|[研发中心]|[推进中心]|[传媒])+', obj[index]):
            continue
        if re.search(r'\.[\s ]*公司', obj[index]):
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
    iden_strs=(
               (r'(.*\d+年{0,1}的)?(.*[：，,。]+)?(.*隶?属于)?(.*\.\s+)?(.+?有限公司)',4),
               (r'(.*\d+年?的)?(.*[：，,。]+)?(.+?研发中心)',2),
               (r'(.*\d+年?的)?(.*[：，,。]+)?是?(.+?集团)',2),
               (r'(.*\d+年?的)?(.*[：，,。]+)?(.*\.\s+)?(.+?公司)',3), 
               (r'(.*\d+年?的)?(.*[：，,。]+)?(.+?推进中心)', 2),
               (r'(.*\d+年?的)?(.*[：，,。]+)?(.+?传媒)' ,2)
            )
    for iden_str,n in iden_strs:
        r = re.findall(iden_str, html)
        if r:
            company=handle_company_name_use_black_data(r, n)
            n=company.find('"')
            if n!=-1:
                return company[n+1:]

            return company
    return "未识别的公司"
# 

def get_work_citys(html):
    """
    获取工作城市
    :param html: 一段字符串
    :return:
    """
    html = BeautifulSoup(html, "html.parser").get_text()
    # r = re.findall(r'(工作地[点]?[:：]?){1}(可选：)?(.*)', html)
    # if r and r[0][2]:
    #     return re.split(r'[#,、，\s]', r[0][2])
    # return []

    r = []
    for city in citys:
        if html.find(city) != -1:
            r.append(city)
    return r


def get_work_position(html):
    """
    获取职位
    :param html: 一段字符串
    :return:
    """
    html = BeautifulSoup(html, "html.parser").get_text()
    r = []
    for p in positions:
        if html.find(p) != -1:
            r.append(p)
    return r


def get_real_time(time_str):
    """
    获取标准的时间
    :param time_str:
    :return:
    """
    time_str = time_str.replace('.', '-')
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

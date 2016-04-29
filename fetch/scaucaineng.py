# coding:utf-8


"""
抓取材料与能源学院招聘信息
@author: coffeesign
2016.04.28

抓取入口：http://xy.scau.edu.cn/caineng/xnyxy/Article/ShowClass.asp?ClassID=182
"""

url_hire = "http://xy.scau.edu.cn/caineng/xnyxy/Article/ShowClass.asp?ClassID=182"
url_host = "http://xy.scau.edu.cn/"

from bs4 import BeautifulSoup
import requests
from tools import *
def get_message_title_and_url_list(html):
    """
    提取兼职信息列表的信息标题和跳转地址
    :param html:
    :return:
    """
    result = []
    soup = BeautifulSoup(html, "html.parser")
    a_s = soup.select("table a")
    for a in a_s:
        title = a.text
        link = a.attrs['href']
        result.append((title,link))
    return result

def get_message_jobs(url):
    """
    获取招聘信息
    """
    html = get_html(url)
    company_name = get_company_name(html)
    work_city = get_work_citys(html)
    work_position = get_work_position(html)
    return text_filter(company_name)

def get_html(url):
    response = requests.get(url)
    return response.content

def test():
    html = get_html(url_hire)
    infos = get_message_title_and_url_list(html)
    for name,url in infos:
        print(get_message_jobs(url_host+url))

if __name__ == '__main__':
    test()
    # get_html()

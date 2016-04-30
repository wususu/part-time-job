# coding:UTF-8


"""
抓取水利学院的招聘信息
@author: yubang
2016.04.30

抓取入口：http://xy.scau.edu.cn/slxy/list.asp?id=35&page=1
"""


from bs4 import BeautifulSoup
from lib import tools
import requests


message_url = 'http://xy.scau.edu.cn/slxy/list.asp?id=35&page=%d'
url_prefix = 'http://xy.scau.edu.cn/slxy/'


def get_title_and_link_list(html):
    """
    提取标题和链接
    :param html:
    :return:
    """
    global url_prefix
    soup = BeautifulSoup(html, "html.parser")
    div_label = soup.find('div', {"class": 'list_4'})
    if not div_label:
        return None

    messages = []
    lis = div_label.find_all('li')
    for li_obj in lis:
        span_label = li_obj.find('span')
        a_label = li_obj.find('a')
        font_label = li_obj.find('font')
        if not span_label or not a_label or not font_label or 'href' not in a_label.attrs:
            continue
        messages.append({"title": font_label.string, "web_url": url_prefix + a_label['href'], "release_time": span_label.string})
    return messages


def get_all_jobs():
    """
    获取最近的招聘信息
    :return:
    """
    global message_url
    messages = []
    page = 1
    while page <= 5:
        url = message_url % page
        response = requests.get(url)
        if response.status_code != 200:
            continue
        response.encoding = 'gbk'
        objs = get_title_and_link_list(response.text)
        messages.extend(objs)
        if len(objs) < 18:
            break
        page += 1
    messages = list(map(handle_job_message, messages))
    return messages


def handle_job_message(obj):
    """
    处理兼职信息
    :param obj:
    :return:
    """
    response = requests.get(obj['web_url'])
    if response.status_code != 200:
        return obj
    response.encoding = 'gbk'
    obj['web_html'] = response.text
    obj['company'] = tools.get_company_name(obj['web_html'])
    obj['position'] = tools.get_work_position(obj['web_html'])
    obj['work_city'] = tools.get_work_citys(obj['web_html'])
    return obj


if __name__ == '__main__':
    with open('../debug_html/6.html', 'r') as fp:
        print(get_title_and_link_list(fp.read()))
    print(get_all_jobs())

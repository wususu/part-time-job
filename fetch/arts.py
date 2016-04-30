# coding:UTF-8


"""
抓取华农艺术学院的招聘信息
@author: yubang
2016-04.29

抓取入口：http://202.116.162.1:9000/news_list.php?id=398&page=1
"""


from bs4 import BeautifulSoup
from lib import tools
import requests


web_url = 'http://202.116.162.1:9000/news_list.php?id=398&page='
message_url_prefix = 'http://202.116.162.1:9000/'


def handle_job_message(obj):
    """
    处理兼职信息
    :param obj:
    :return:
    """
    response = requests.get(obj['web_url'])
    if response.status_code != 200:
        return obj

    obj['web_html'] = response.content
    obj['company'] = tools.get_company_name(obj['web_html'])
    obj['position'] = tools.get_work_position(obj['web_html'])
    obj['work_city'] = tools.get_work_citys(obj['web_html'])
    return obj


def get_message_title_and_url_list(html):
    """
    提取兼职信息列表的信息标题和跳转地址
    :param html:
    :return:
    """
    global message_url_prefix
    soup = BeautifulSoup(html, "html.parser")
    div_label = soup.find('div', {"class": 'div_14'})
    if not div_label:
        return None
    li_labels = div_label.find_all('li')
    r = []

    for obj in li_labels:
        span_label = obj.find('span')
        a_label = obj.find('a')
        if not span_label or not a_label or 'href' not in a_label.attrs:
            continue
        r.append({"web_url": message_url_prefix + a_label['href'], "title": a_label.string, "release_time": span_label.string})

    return r


def get_all_page_of_work():
    """
    获取所有页
    :return:
    """
    global web_url
    page = 1
    messages = []
    while page < 20:
        url = web_url + str(page)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        objs = get_message_title_and_url_list(response.content)
        messages.extend(objs)

        if len(objs) < 15:
            break
        page += 1
    messages = list(map(handle_job_message, messages))
    return messages

if __name__ == '__main__':
    with open('../debug_html/3.html', 'r') as fp:
        get_message_title_and_url_list(fp.read())
    get_all_page_of_work()

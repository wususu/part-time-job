# coding:UTF-8


"""
抓取公共管理学院的招聘信息
@author: yubang
2016.04.30

抓取入口：http://xy.scau.edu.cn/gongguan/new/jy/
"""


from bs4 import BeautifulSoup
from lib import tools, dao
from lib.logging_lib import log
import requests


message_url_prefix = 'http://xy.scau.edu.cn'
first_url = 'http://xy.scau.edu.cn/gongguan/new/jy/'


def get_tile_and_link_lists(html):
    """
    获取标题和链接列表
    :param html:
    :return:
    """
    global message_url_prefix
    soup = BeautifulSoup(html, "html.parser")
    div_label = soup.find('div', {"class": 'info'})
    if not div_label:
        return None
    messages = []
    trs = div_label.find_all('tr')
    for tr_obj in trs:
        tds = tr_obj.find_all('td')
        if len(tds) != 3:
            continue

        a_lable = tds[1].find_all('a')[1]
        font_text = tds[2].get_text()
        if not a_lable or not font_text or 'href' not in a_lable.attrs or 'title' not in a_lable.attrs:
            continue
        messages.append({"title": a_lable['title'], "web_url": message_url_prefix + a_lable['href'], "release_time": font_text})

    return messages


def handle_job_message(obj):
    """
    处理兼职信息
    :param obj:
    :return:
    """
    tools.sleep_some_time()
    response = requests.get(obj['web_url'])
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (obj['web_url'], response.status_code))
        return obj
    response.encoding = 'gbk'
    obj['web_html'] = response.text
    obj['company'] = tools.get_company_name(obj['web_html'])
    obj['position'] = tools.get_work_position(obj['web_html'])
    obj['work_city'] = tools.get_work_citys(obj['web_html'])
    return obj


def get_all_page_of_job():
    """
    获取每一页的招聘信息
    :return:
    """
    global first_url
    response = requests.get(first_url)
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (first_url, response.status_code))
        return None
    response.encoding = 'gbk'
    objs = get_tile_and_link_lists(response.text)
    objs = list(map(handle_job_message, objs))
    return objs


def init():
    objs = get_all_page_of_job()
    for obj in objs:
        dao.add_a_job(obj['title'], obj['company'], obj['web_url'], obj['work_city'], '华农水利学院官网', obj['position'],
                      obj['release_time'], obj['web_html'])


if __name__ == '__main__':
    with open('../debug_html/4.html', 'r') as fp:
        objs = get_tile_and_link_lists(fp.read())
        print(objs)
    print(get_all_page_of_job())
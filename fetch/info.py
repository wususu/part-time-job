# coding:UTF-8


"""
抓取数学与信息学院招聘信息
@author: yubang
2016.04.30

抓取入口：http://info.scau.edu.cn/category-11.html?key=&cid=&value=&selGrade=&name=&selUserType=&searchType=&searchText=&selClazzName=&pageSize=20&pager.offset=0
"""


from bs4 import BeautifulSoup
from lib import tools, dao
from lib.logging_lib import log
import requests


message_url = 'http://info.scau.edu.cn/category-11.html?key=&cid=&value=&selGrade=&name=&selUserType=&searchType=&searchText=&selClazzName=&pageSize=20&pager.offset=%d'
message_url_prefix = 'http://info.scau.edu.cn'


def get_title_and_link_list(html):
    """
    提取标题和链接
    :param html:
    :return:
    """
    global message_url_prefix
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', {"class": 'table table-bordered table-hover'})
    if not table:
        return None

    messages = []
    trs = table.find_all("tr")
    for tr_obj in trs:
        a_label = tr_obj.find('a')
        tds = tr_obj.find_all('td')
        if len(tds) != 4:
            continue
        if not a_label or 'href' not in a_label.attrs:
            continue
        messages.append({"title": tds[0].string, "release_time": tds[3].string, "web_url": message_url_prefix + a_label['href']})

    return messages


def get_all_page_of_job():
    """
    获取最近的招聘信息
    :return:
    """
    global message_url
    messages = []
    page = 1
    while page <= 1:
        url = message_url % (page - 1) * 20
        response = requests.get(url)
        if response.status_code != 200:
            log.error("网址（%s）无法访问，状态码：%d" % (url, response.status_code))
            continue
        objs = get_title_and_link_list(response.content)
        messages.extend(objs)

        if len(objs) < 20:
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
    tools.sleep_some_time()
    response = requests.get(obj['web_url'])
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (obj['web_url'], response.status_code))
        return obj

    obj['web_html'] = response.content
    obj['company'] = tools.get_company_name(obj['web_html'])
    obj['position'] = tools.get_work_position(obj['web_html'])
    obj['work_city'] = tools.get_work_citys(obj['web_html'])
    return obj


def init():
    objs = get_all_page_of_job()
    for obj in objs:
        dao.add_a_job(obj['title'], obj['company'], obj['web_url'], obj['work_city'], '华农水利学院官网', obj['position'],
                      obj['release_time'], obj['web_html'])


if __name__ == '__main__':
    with open('../debug_html/5.html', 'r') as fp:
        get_title_and_link_list(fp.read())
    print(get_all_page_of_job())

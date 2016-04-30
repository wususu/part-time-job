# coding:UTF-8


"""
抓取电子工程学院招聘信息
@author: yubang
2016.04.28

抓取入口：http://job.scautiu.com/news/newsListClass.aspx?ncid=2
"""


from bs4 import BeautifulSoup
from lib import tools
import requests


message_url_prefix = 'http://job.scautiu.com/news/'
first_html_url = 'http://job.scautiu.com/news/newsListClass.aspx?ncid=2'


def get_search_form(html):
    """
    获取搜索所需要的隐藏字段
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find('form', {"id": 'form1'})
    if not form:
        return None

    hiddens = form.find_all('input', {"type": 'hidden'})
    r = {}
    for obj in hiddens:
        if 'name' not in obj.attrs or 'value' not in obj.attrs:
            continue
        r[obj['name']] = obj['value']
    return r


def get_message_title_and_url_list(html):
    """
    提取兼职信息列表的信息标题和跳转地址
    :param html:
    :return:
    """
    global message_url_prefix
    soup = BeautifulSoup(html, "html.parser")
    message_div = soup.find('div', {"class": 'mainContent fr'})
    if not message_div:
        return None, None
    objs = message_div.find_all('a')
    r = []
    for obj in objs:
        title_label = obj.find('h4')
        release_time_label = obj.find('span')
        if not title_label or not release_time_label or 'href' not in obj.attrs:
            continue
        r.append({"title": title_label.string, "release_time": release_time_label.string, "web_url": message_url_prefix + obj['href']})
    return r


def get_all_page_html():
    """
    获取若干页
    :return:
    """
    global first_html_url
    # 获取第一页信息
    response = requests.get(first_html_url)
    if response.status_code != 200:
        return None

    html = response.content
    if not html:
        return None

    messages = get_message_title_and_url_list(html)

    page = 2
    form_data = get_search_form(html)
    while(page < 50):
        form_data['__EVENTTARGET'] = 'ctl00$cph_content_temp$DataPager1$ctl01$ctl0%d' % (page - 1)
        response = requests.post(first_html_url, form_data)

        if response.status_code != 200:
            page += 1
            continue

        # 更新form隐藏字段
        html = response.content
        form_data = get_search_form(html)

        temp_messages = get_message_title_and_url_list(html)
        messages.extend(temp_messages)

        if not temp_messages or len(temp_messages) < 10:
            break

        page += 1
    messages = list(map(handle_job_message, messages))
    return messages


def handle_job_message(obj):
    """
    处理兼职信息具体信息
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


def test():
    with open('../debug_html/1.html', 'r') as fp:
        print(get_message_title_and_url_list(fp.read()))
    with open('../debug_html/1.html', 'r') as fp:
        print(get_search_form(fp.read()))
    # print(get_all_page_html())


if __name__ == '__main__':
    test()

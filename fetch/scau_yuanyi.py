#爬取园艺学院 注：网页为“gb2312编码”
import re
from bs4 import BeautifulSoup
import requests
from lib import tools,dao
from lib.logging_lib import log


url_first = 'http://xy.scau.edu.cn/yyx/web/html/working/info/Index.html'
source_url = 'http://xy.scau.edu.cn/'
page_url = 'http://xy.scau.edu.cn/yyx/web/html/working/Index_'


def Get_html(url):
    """
    获取html
    :param url:
    :return:
    """
    req = requests.get(url)
    if req.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, req.status_code))
        return None
    html=req.content.decode('gb2312','ignore').encode('utf8')          #解码并编码为utf8
    return html


def get_title(html):
    """
    获取标题
    :param html:
    :return:
    """
    html = BeautifulSoup(html,"html.parser").get_text()
    try:
        x = re.findall(r'^(.+?)-华南农业大学园艺学院',html)
        return x[0]
    except:
        return '提取失败'


def get_date(html):
    """
    提取日期
    :param html:
    :return:
    """
    html = BeautifulSoup(html,"html.parser").get_text()
    #print(html)
    try:
        x = re.findall(r'\s作者：(.*?)来源：(.*?)日期：(\d{4}-\d{1,2}-\d{1,2})(.*?)人气',html)
        return x[0][2]
    except:
        return '提取失败'


def get_job_url(url):
    """
    获取页码数并采集各页url
    :param url:
    :return:
    """
    url_list = []
    html_1 =Get_html(url)
    html_2 = BeautifulSoup(html_1,"html.parser")
    for data  in html_2.findAll('a',href = re.compile("^/yyx/web/html/working/info/([0-9]+).html$")):
        url = source_url + data.attrs['href']
        url_list.append(url)
    return url_list


def get_pages(html):
    """
    1.判断页数
    2.收集所有页面url
    :param html:
    :return:
    """
    all_url_list = []
    html_world = BeautifulSoup(html,"html.parser").get_text()
    x = re.findall(r'.*下一页(.*?)页次：([0-9]+?)/([0-9]+)',html_world)
    for i in range(int(x[0][2])):
        a = i+1
        if a == 1:
            url = 'http://xy.scau.edu.cn/yyx/web/html/working/index.html'
        else:
            url = page_url + str(a) + '.html'
            all_url_list.extend(get_job_url(url))
    return all_url_list


def handle_all_data(url):
    """
    获取每一条信息
    :param url:
    :return:
    """
    tools.sleep_some_time()
    zhaopin_data = {}
    html = Get_html(url)
    zhaopin_data['web_url'] = url
    zhaopin_data['web_html'] = html
    zhaopin_data['title'] = get_title(html)
    zhaopin_data['release_time'] = tools.get_real_time(get_date(html))
    zhaopin_data['company'] = tools.get_company_name(html)
    zhaopin_data['position'] = tools.get_work_position(html)
    zhaopin_data['work_city'] = tools.get_work_citys(html)
    zhaopin_data['message_source'] = '华农园艺学院官网'
    print(zhaopin_data['title'],zhaopin_data['release_time'],zhaopin_data['message_source'],zhaopin_data['company'])
    return zhaopin_data


def get_all_data():
    final_data = []
    html = Get_html(url_first)
    all_url_list = get_pages(html)
    for url in all_url_list:
        final_data.append(handle_all_data(url))
    return final_data


def init():
    objs = get_all_data()
    for obj in objs:
        dao.add_a_job(obj['title'], obj['company'], obj['web_url'], obj['work_city'], obj['message_source'], obj['position'],
                      obj['release_time'], obj['web_html'])


def test():
    print(len(get_all_data()))


if __name__ == '__main__':
    test()

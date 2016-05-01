#农学院爬虫
from lib import tools,dao
import requests
from bs4 import BeautifulSoup
import re
from lib.logging_lib import log


url_first = 'http://xy.scau.edu.cn/nxy/cx/Ch/xwzx.asp?SortID=57&SortPath=0,57,&Page='  #入口

def get_date(html):
    """
    获取发布日期
    :param url:
    :return:
    """
    html=BeautifulSoup(html,"html.parser").get_text()
    date = re.findall(r'.*新闻来源(.+?)更新时间：(\d{4}-\d{1,2}-\d{1,2}).*',html)
    if date:
        return date[0][1]
    return "提取失败"


def get_title(html):
    """
    获取标题
    :param url:
    :return:
    """
    html=BeautifulSoup(html,"html.parser")
    title = html.find("td",{"align":"center","colspan":"2","height":"40"}).text
    if title:
        return title
    return "提取失败"


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
    html=req.content
    return html

def get_pages(url):
    """
    获取招聘url
    """
    html = Get_html(url)
    html=BeautifulSoup(html,"html.parser")
    pages_url= []
    try:
        for data in html.findAll("a",href = re.compile("(xwzxView\.asp\?(.)*)+SortID=57$")):
            url_zhaopin = 'http://xy.scau.edu.cn/nxy/cx/Ch/'+ data.attrs['href']
            pages_url.append(url_zhaopin)
    except:
        print("error")
    return pages_url


def get_url(url_1):
    """
   获取页码数并采集各页url
    :param url_1:
    :return:
    """
    url_2 = 'http://xy.scau.edu.cn/nxy/cx/Ch/xwzx.asp?SortID=57&SortPath=0,57,' #用于匹配页数
    html = Get_html(url_2)
    html=BeautifulSoup(html,"html.parser")
    list_url=[]
    html_fix = html.get_text()
    a = re.findall(r'.*共计(.*?)页次：1/([0-9]{1,}).每页',html_fix)
    for x in range(int(a[0][1])):
        x = x+1
        url = url_1 + str(x)
        list_url.extend(get_pages(url))
    return list_url


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
    zhaopin_data['message_source'] = '华农农学院官网'
    print(zhaopin_data['title'],zhaopin_data['release_time'],zhaopin_data['message_source'],zhaopin_data['company'])
    return zhaopin_data


def get_all_data():
    final_data = []  # 总信息
    all_url_list = get_url(url_first)
    for url in all_url_list:
        final_data.append(handle_all_data(url))
    return final_data

def init():
    objs =  get_all_data()
    for obj in objs:
        dao.add_a_job(obj['title'], obj['company'], obj['web_url'], obj['work_city'], obj['message_source'], obj['position'],
                      obj['release_time'], obj['web_html'])


def text():

    #print(final_data)
    print(get_all_data())

if __name__ == '__main__':
    text()

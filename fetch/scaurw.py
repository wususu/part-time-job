# coding:utf-8


"""
抓取人文与法学学院招聘信息
@author: coffeesign
2016.04.28

抓取入口：http://rw.scaunet.com/Web/Article.aspx?cid=1081
"""

url_hire = "http://rw.scaunet.com/Web/Article.aspx?cid=1081&page={0}"
url_host = "http://rw.scaunet.com/Web/"

from bs4 import BeautifulSoup
import requests
from tools import *
from gevent import monkey;monkey.patch_socket()
from gevent.pool import Pool
def get_message_title_and_url_list(page):
    """
    提取第page页的兼职信息列表的信息标题、跳转地址和发布时间
    :param html:
    :return:
    """
    url=url_hire.format(page)
    html=get_html(url)
    result = []
    soup = BeautifulSoup(html, "html.parser")
    a_s = soup.select("table a")
    for a in a_s:
        title = a.text
        link = a.attrs['href']
        result.append((title,link))
    return result

def get_page_num():
    url=url_hire.format(1)
    html=get_html_t(url)
    page_re=re.findall(r"总：(\d+) 页",html)
    return int(page_re[-1])

def get_message_jobs(url):
    """
    获取招聘信息
    """
    info={}
    html = get_html(url)
    company_name = get_company_name(html)
    work_city = get_work_citys(html)
    work_position = get_work_position(html)
    release_time=get_release_time(html)

    info['release_time']=release_time
    info['web_html']=html
    info['company']=company_name
    info['work_city']=work_city
    info['position']=work_position
    return info


def fetch():
    result=[]
    infos = get_message_title_and_url_list(1)

    def tmp(info):
        title,link=info
        url=url_host+link
        info={}
        info['title']=text_filter(title)
        info['web_url']=url
        info['message_source']="生命科学学院官网"
        info['job_type']=0
        info['authentication']=0
        info.update(get_message_jobs(url))
        result.append(info)
        print(info['title'],info['release_time'])

    p=Pool(10)
    p.map(tmp,infos)
    return result

if __name__ == '__main__':
    fetch()
    # print(get_page_num())
# coding:utf-8


"""
抓取生命科学学院招聘信息
@author: coffeesign
2016.04.28

抓取入口：http://life.scau.edu.cn/news-subject-31.asp?navId=52
"""

url_hire = "http://life.scau.edu.cn/news-subject-31.asp?navId=52&page={0}"
url_host = "http://life.scau.edu.cn"

from bs4 import BeautifulSoup
import requests
import re
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
    lis = soup.select(".nav-news-list li")
    for li in lis:
        a=li.select("a")[0]
        title = a.text
        link = a.attrs['href']

        release_time=li.select(".news-time")[0].text
        result.append((title,link,release_time))
    return result

def get_page_num():
    url=url_hire.format(1)
    html=get_html_t(url)
    page_re=re.findall(r"navId=52\">(\d+)</a>",html)
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

    info['web_html']=html
    info['company']=company_name
    info['work_city']=work_city
    info['position']=work_position
    return info


def fetch():
    result=[]
    n=get_page_num()

    import csv
    f=open("life.csv","w")

    writer=csv.writer(f)
    def tmp(info):
        title,link,release_time=info
        url=url_host+link
        info={}
        info['title']=title
        info['web_url']=url
        info['release_time']=release_time
        info['message_source']="生命科学学院官网"
        info['job_type']=0
        info['authentication']=0
        info.update(get_message_jobs(url))
        result.append(info)
        writer.writerow((info['title'],info['company'],info['release_time'],info['work_city'],info['web_url']))
        print(info['title'],info['company'],info['release_time'])

    for i in range(1,n+1):
        infos = get_message_title_and_url_list(i)
        p=Pool(20)
        p.map(tmp,infos)

    f.close()
    return result

if __name__ == '__main__':
    fetch()
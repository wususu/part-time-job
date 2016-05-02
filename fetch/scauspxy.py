# coding:utf-8


"""
抓取食品学院招聘信息
@author: coffeesign
2016.04.28

抓取入口：http://xy.scau.edu.cn/spxy/career/title.asp?id=39
"""

url_hire = "http://xy.scau.edu.cn/spxy/career/title.asp?id=39&page={0}"
url_host = "http://xy.scau.edu.cn/spxy/career/"

from bs4 import BeautifulSoup
import requests
from lib import tools
from lib.coffeesign_tools import *
from lib import dao

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
        title = a.select("font")[0].text
        link = a.attrs['href']
        result.append((title,link))
    return result

def get_page_num():
    url=url_hire.format(1)
    html=get_html_t(url)
    page_re=re.findall(r"\&page\=(\d+)",html)
    return int(page_re[-1])

def get_message_jobs(url):
    """
    获取招聘信息
    """
    info={}
    html = get_html_t(url)
    company_name = get_company_name(html)
    work_city = tools.get_work_citys(html)
    work_position = tools.get_work_position(html)
    release_time = get_release_time(html)

    info['release_time']=tools.get_real_time(release_time)
    info['web_html']=html
    info['company']=company_name
    info['work_city']=work_city
    info['position']=work_position
    return info


def fetch():
    result=[]
    infos = get_message_title_and_url_list(1)

    for info in infos:
        tools.sleep_some_time()
        title,link=info
        url=url_host+link
        info={}
        info['title']=title
        info['web_url']=url
        info['message_source']="食品学院官网"
        info['job_type']=0
        info['authentication']=0
        info.update(get_message_jobs(url))
        result.append(info)
        print(info['title'],info['company'],info['release_time'])
    

    return result

def init():
    infos = fetch()
    for info in infos:
        dao.add_a_job(info['title'], info['company'], info['web_url'], info['work_city'], info['message_source'], info['position'],
                      info['release_time'], info['web_html'])
if __name__ == '__main__':
    print(fetch())
    # print(get_page_num())
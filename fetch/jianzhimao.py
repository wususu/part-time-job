import requests
from bs4 import BeautifulSoup
import re
from tools import get_position
from datetime import datetime,timedelta
first_url = 'http://guangzhou.jianzhimao.com/dbx_zbx_0/index'


def get_html(url):
    rep = requests.get(url)
    if rep.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, rep.status_code))
        return None
    html = rep.content
    return html

def get_urls(page_url):
    """
    获取单页页的兼职链接标题
    :param page_url:
    :return:
    """
    jobs_data = []

    html = get_html(page_url)
    html = BeautifulSoup(html,"html.parser")
    data = html.findAll("a",href = re.compile(r'/job/[0-9a-zA-Z]{16}.html'))

    for i in data :
        job_data = {}
        url = "http://guangzhou.jianzhimao.com" + i.attrs['href']
        job_data['web_url'] = url
        title = i.attrs["title"]
        job_data['title'] = title
        jobs_data.append(job_data)
    return jobs_data

def get_all_urls(first_url):
    """
    获取所有url,title
    :param first_url:
    :return:
    """
    jobs_data = []
    for i in range(11):
        i += 1
        page_url = first_url + str(i) + ".html"
        print(page_url)
        jobs_data += get_urls(page_url)
        print(len(jobs_data))
    # for i in jobs_data:
    #     print(i)
    return jobs_data
url1 = "http://guangzhou.jianzhimao.com/job/V2c2TUlIRklZL2c9.html"
url2 = "http://guangzhou.jianzhimao.com/job/UFVBZmF6TVgwakk9.html"
def get_time(html):
    # html = get_html(url)
    html = BeautifulSoup(html,"html.parser")
    a = html.findAll("span",{"class":"date right yellow"})[0].get_text()
    if "昨天" in a:
        day = 1
    elif "前天" in a:
        day = 2
    elif "前" in a:
        day = 0
    else:
        day = -1
        date = 0
    if day != -1:
        date = datetime.now().date() - timedelta(days=day)
    return date

def get_company(url):
    html = get_html(url)
    html = str(BeautifulSoup(html, "html.parser"))
    print(html)
    company = re.findall(r'(.+)>发布者: (.+)?<(.*)', html)[0][1]
    return company
# get_time(url1)
# get_all_urls(first_url)
get_company(url1)
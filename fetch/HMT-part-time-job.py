import requests
from bs4 import BeautifulSoup
import re
from tools import get_position

url = 'http://hometown.scau.edu.cn/bbs/forum.php?mod=forumdisplay&fid=142&page='
url2 = "http://hometown.scau.edu.cn/bbs/forum.php?mod=viewthread&tid=923991&extra=page%3D1"


def get_html(url):
    req = requests.get(url)
    if req.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, req.status_code))
        return None
    html = req.content
    return html


def get_urls(page_url):
    """
    获取单页页的兼职连接
    :param page_url:
    :return:
    """
    urls = []
    not_urls = []
    html = get_html(page_url)
    html = BeautifulSoup(html,"html.parser")
    for data in html.findAll('a',href = re.compile("^forum\.php\?mod=viewthread&tid=(\d{6})&extra=page%3D\d$")):
        url = "http://hometown.scau.edu.cn/bbs/" + data.attrs['href']
        try:
            if '本版置顶主题 - 新窗口打开' == data.attrs['title']:
                not_urls.append(url)
        except: pass
        if url not in urls and url not in not_urls:
            urls.append(url)
    return urls



def get_title(url):
    html = get_html(url)
    html = BeautifulSoup(html, "html.parser")

    title = html.find('span',{"id":"thread_subject"}).text
    return title


def get_time(url):
    html = get_html(url)
    html = str(BeautifulSoup(html, "html.parser"))
    # print(html)
    try:
        time = re.findall(r'.*>发表于 (\d{4}-\d{1,2}-\d{1,2}) \d{1,2}:\d{1,2}:\d{1,2}<.*', html)[0]
    except : time = re.findall(r'.*发表于 <span title="(\d{4}-\d{1,2}-\d{1,2}) \d{1,2}:\d{1,2}:\d{1,2}.*">',html)[0]
    # print(time)
    return time


def get_all_data(url):
    urls = []
    jobs_data = []
    job_data = {}
    for i in range(10):
        page_url = url + str(i)
        urls = urls + get_urls(page_url)
    for i in urls:
        html =get_html(i)
        job_data['url'] = i
        job_data['web_html'] = html
        job_data['title'] = get_title(i)
        job_data['time'] = get_time(i)
        job_data['work_position'] = get_position(html)
        jobs_data.append(job_data)
        print("工作: ", job_data['title'])
        print("发布时间: ", job_data['time'])
        print("连接: ", job_data['url'])
        print("职位: ", job_data['work_position'])
    print(len(jobs_data))
    # for i in jobs_data:
    #     print("工作: ",i['title'])
    #     print("发布时间: ",i['time'])
    #     print("连接: ", i['url'])
    #     print("职位: ",i['work_position'])


get_all_data(url)

# urrl = "http://hometown.scau.edu.cn/bbs/forum.php?mod=viewthread&tid=924063&extra=page%3D1"


# get_time(urrl)




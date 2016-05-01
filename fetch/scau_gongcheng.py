#scau 工程学院
import re
import requests
from bs4 import BeautifulSoup
from lib import tools,dao
from lib.logging_lib import log


zhaopin_data = {}
url_first = 'http://gcxy.scau.edu.cn/Channel-transfer-cid-13' #入口
page_url = 'http://gcxy.scau.edu.cn/Channel-transfer-cid-13-p-'
data_source_url = 'http://gcxy.scau.edu.cn'


def Get_html(url):
    req = requests.get(url)
    if req.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, req.status_code))
        return None
    html=req.content
    return html


def get_pages(html):
    """
    1.判断页数
    2.收集所有页面url
    :param html:
    :return:
    """
    list_pages = []
    html_world = BeautifulSoup(html,"html.parser")
    x =re.findall(re.compile('.*/Channel-transfer-cid-\d\d-p-([0-9]*)'),str(html_world))
    for i in range(int(x[0])):
        a =i+1
        url = page_url + str(a)
        list_pages.extend(
            get_job_url(url))
    return list_pages


def get_job_url(url):
    """
    收集本页面所有工作的url
    :return:
    """
    list_url = []
    html_1 =Get_html(url)
    html_2 = BeautifulSoup(html_1,"html.parser")
    for data in html_2.findAll("a",href = re.compile("/article-transfer-pid-\d\d\d\d")):
        data_url = data_source_url+data.attrs['href']
        list_url.append(data_url)
    return list_url


def get_title(html):
    html = BeautifulSoup(html,"html.parser")
    try:
        title = html.find("h2",{"class":"article-content-title"}).text
        return title
    except:
        return '提取失败'


def get_date(html):
    html_world = BeautifulSoup(html, "html.parser").get_text()
    try:
        x = re.findall(r'作者：(.+)时间：(\d\d\d\d-\d{1,2}-\d{1,2}).{2}来源',html_world)
        date = x[0][1]
        return date
    except:
        return '提取失败'


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
    zhaopin_data['message_source'] = '华农工程学院官网'
    print(zhaopin_data['title'],zhaopin_data['release_time'],zhaopin_data['message_source'],zhaopin_data['company'])
    return zhaopin_data


def get_all_data():
    final_data = []
    html = Get_html(url_first)
    all_url_list = get_pages(html)
    for url in all_url_list:
        final_data.append(handle_all_data(url))
    return final_data


def text():

    print(len(get_all_data()))

def init():
    objs = get_all_data()
    for obj in objs:
        dao.add_a_job(obj['title'], obj['company'], obj['web_url'], obj['work_city'], obj['message_source'], obj['position'],
                      obj['release_time'], obj['web_html'])

if __name__ == '__main__':
    text()

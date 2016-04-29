#scau 工程学院
import re
import requests
from bs4 import BeautifulSoup
from part_time_and_work.fetch import tools

final_data = []
zhaopin_data = {}
url_first = 'http://gcxy.scau.edu.cn/Channel-transfer-cid-13' #入口
page_url = 'http://gcxy.scau.edu.cn/Channel-transfer-cid-13-p-'
data_source_url = 'http://gcxy.scau.edu.cn'


def Get_html(url):
    req = requests.get(url)
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
    try:
        title = html.find("h2",{"class":"article-content-title"}).text
        return title
    except:
        return '提取失败'

def get_date(html):
    html_world = html.get_text()
    try:
        x = re.findall(r'作者：(.+)时间：(\d\d\d\d-\d{1,2}-\d{1,2}).{2}来源',html_world)
        date = x[0][1]
        return date
    except:
        return '提取失败'


def get_all_data():
    """
    采集工作信息
    :return:
    """
    #x=1
    html = Get_html(url_first)
    all_url_list = get_pages(html)
    for url in all_url_list:
        html_1 = Get_html(url)
        html = BeautifulSoup(html_1,"html.parser")
        zhaopin_data['web_url'] = url
        zhaopin_data['web_html'] = html_1
        zhaopin_data['title'] = get_title(html)
        zhaopin_data['release_time'] = get_date(html)
        zhaopin_data['company'] = tools.get_company_name(html_1)
        zhaopin_data['position'] = tools.get_work_position(html_1)
        zhaopin_data['work_city'] = tools.get_work_citys(html_1)
        zhaopin_data['message_source'] = ''
        zhaopin_data['job_type'] = ''
        #打印所有信息
        #print("招聘",x,zhaopin_data['title'],zhaopin_data['release_time'],zhaopin_data['web_url'],zhaopin_data['company'])
        #x+=1
        final_data.append(zhaopin_data)
    return final_data


def text():
    get_all_data()
    print(len(final_data))

if __name__ == '__main__':
    text()

import re
from bs4 import BeautifulSoup
import requests
from part_time_and_work.fetch import tools

final_data = []
url_first = 'http://zyhjxy.scau.edu.cn/news.php?a=lists&id=31'
url_work = 'http://zyhjxy.scau.edu.cn/'
url_page = 'http://zyhjxy.scau.edu.cn/news.php?m=home&c=news&a=lists&m=home&c=news&id=31&p='


def Get_html(url):
    req = requests.get(url)
    html=req.content
    return html


def get_title(html):
    """
    获取标题
    :param html:
    :return:
    """
    html = BeautifulSoup(html,"html.parser")
    try:
        title = html.find("h1",{"class":None}).text
        return title
    except:
        return '提取失败'


def get_date(html):
    html = BeautifulSoup(html,"html.parser").get_text()
    try:
        x = re.findall(r'\d\d\d\d年\d{1,2}月\d{1,2}日',html)
        return x[0]
    except:
        return '提取失败'


def get_pages(html):
    """
    1.判断页数
    2.收集所有页面url
    :param html:
    :return:
    """
    all_url_list = []
    html_world = BeautifulSoup(html,"html.parser")
    x = html_world.findAll("a",href = re.compile('/news\.php\?m=home&c=news&a=lists&id=31&p=[0-9]*') )
    for i in range(len(x)):
        x = i + 1
        url = url_page + str(x)
        all_url_list.extend(get_job_url(url))

    return all_url_list


def get_job_url(url):
    """
    获取页码数并采集各页url
    :param url:
    :return:
    """
    url_list = []
    html_1 =Get_html(url)
    html_2 = BeautifulSoup(html_1,"html.parser")
    for data in html_2.findAll('a',href = re.compile('/news\.php\?id=[0-9]{2,}')):
        url = url_work + data.attrs['href']
        url_list.append(url)
    return url_list


def get_all_data():
    zhaopin_data = {}
    html = Get_html(url_first)
    all_url_list = get_pages(html)
    x=0
    for url in all_url_list:
        x+=1
        html = Get_html(url)
        zhaopin_data['web_url'] = url
        zhaopin_data['web_html'] = html
        zhaopin_data['title'] = get_title(html)
        zhaopin_data['release_time'] = get_date(html)
        zhaopin_data['company'] = tools.get_company_name(html)
        zhaopin_data['position'] = tools.get_work_position(html)
        zhaopin_data['work_city'] = tools.get_work_citys(html)
        zhaopin_data['message_source'] = ''
        zhaopin_data['job_type'] = ''
        print(x,zhaopin_data['title'],zhaopin_data['company'],zhaopin_data['release_time'],zhaopin_data['web_url'])
        final_data.append(zhaopin_data)


def text():
    get_all_data()
    print(len(final_data))


if __name__ == '__main__':
    text()

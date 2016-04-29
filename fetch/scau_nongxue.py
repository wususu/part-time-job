#农学院爬虫
from part_time_and_work.fetch import tools
import requests
from bs4 import BeautifulSoup
import re

final_data=[] #总信息
url_1 = 'http://xy.scau.edu.cn/nxy/cx/Ch/xwzx.asp?SortID=57&SortPath=0,57,&Page='  #入口

def get_date(url):
    """
    获取发布日期
    :param url:
    :return:
    """
    response = requests.get(url)
    html=response.content
    html=BeautifulSoup(html,"html.parser").get_text()
    date = re.findall(r'.*新闻来源(.+?)更新时间：(\d{4}-\d{1,2}-\d{1,2}).*',html)
    if date:
        return date[0][1]
    return "提取失败"


def get_title(url):
    """
    获取标题
    :param url:
    :return:
    """
    html = Gethtml(url)
    title = html.find("td",{"align":"center","colspan":"2","height":"40"}).text
    if title:
        return title
    return "提取失败"


def Gethtml(url):
    """
    获取html
    :param url:
    :return:
    """
    req = requests.get(url)
    html=req.content
    html=BeautifulSoup(html,"html.parser")
    return html

def get_page(url):
    """
    获取招聘url
    """
    bsobj = Gethtml(url)
    pages_url= []
    try:
        for data in bsobj.findAll("a",href = re.compile("(xwzxView\.asp\?(.)*)+SortID=57$")):
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
    html = Gethtml(url_2)
    list_url=[]
    html_fix = html.get_text()
    a = re.findall(r'.*共计(.*?)页次：1/([0-9]{1,}).每页',html_fix)
    for x in range(int(a[0][1])):
        x = x+1
        url = url_1 + str(x)
        list_url.extend(get_page(url))
    return list_url


def get_all_data():
    """
    收集所有信息
    :return:
    """
    data_zaopin={}
    list_url = get_url(url_1)
    for i in range(len(list_url)):
        response = requests.get(list_url[i])
        html = response.content
        data_zaopin['web_html'] = html
        data_zaopin['title'] = get_title(list_url[i])
        data_zaopin['company'] = tools.get_company_name(html)
        data_zaopin['web_url'] = list_url[i]
        data_zaopin['release_time'] = get_date(list_url[i])
        data_zaopin['work_city'] = tools.get_work_citys(html)
        data_zaopin['work_position'] = tools.get_work_position(html)
        data_zaopin['message_source'] = ''
        data_zaopin['job_type'] = ''
        #打印信息
        print(i," ",data_zaopin['release_time'],data_zaopin['title'],data_zaopin['company'],data_zaopin['web_url'])
        final_data.append(data_zaopin)



def text():
    get_all_data()
    #print(final_data)
    print(len(final_data))

if __name__ == '__main__':
    text()

from lib import tools
import requests
from bs4 import BeautifulSoup
import re
from lib.logging_lib import log
def text_filter(text):
    filter_strs=["\xa0","\ufffd","\u200b","\u2022"]
    for filter_str in filter_strs:
        text=text.replace(filter_str,"")
    return text

def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, response.status_code))
    return response.content

def get_html_t(url,coding="utf-8"):
    response = requests.get(url)
    if response.status_code != 200:
        log.error("网址（%s）无法访问，状态码：%d" % (url, response.status_code))

    content=str(response.content)
    r=re.findall("charset=(\w+)\"",content)
    if r:
        coding=r[0].lower()
    response.encoding=coding
    return response.text

def get_release_time(html):
    html = BeautifulSoup(html, "html.parser").get_text()
    r=re.findall(r"(\d{4}\-\d+\-\d+)",html)
    if r:
        return r[0]

    r=re.findall(r"(\d+\-\d+)发布",html)
    if r:
        return r[0]

def handle_title(title):
    pass

def get_company_name(obj):
    name=tools.get_company_name(obj)
    strs=['"','“']
    for _str in strs:
        n=name.find(_str)
        if n!=-1:
            return name[n+1:]
    return name
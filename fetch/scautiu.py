# coding:UTF-8


"""
抓取电子工程学院招聘信息
@author: yubang
2016.04.28

抓取入口：http://job.scautiu.com/news/newsListClass.aspx?ncid=2
"""


from bs4 import BeautifulSoup
import tools

def get_message_title_and_url_list(html):
    """
    提取兼职信息列表的信息标题和跳转地址
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")



def test():
    with open('../debug_html/1.html', 'r') as fp:
        print(get_message_title_and_url_list(fp.read()))

if __name__ == '__main__':
    print("test")

# coding:UTF-8


"""
业务功能封装
2016.04.30
"""


from lib import db_lib, tools
from lib.logging_lib import log
from pymysql import IntegrityError
import hashlib


def add_company(company_name):
    """
    添加企业
    :param company_name: 公司名字
    :return:
    """
    token = hashlib.md5(company_name.encode("UTF-8")).hexdigest()
    sql = "insert ignore into companys(company_name, token, create_time) values(%s, %s, now());"
    return db_lib.update(sql, [company_name, token])


def add_a_job(job_title, job_company, job_url, job_city, job_message_source, job_position, job_release_time, web_html):
    """
    添加一条招聘信息
    :param job_title: 工作标题
    :param job_company: 公司名字
    :param job_url: 跳转的页面地址
    :param job_city: 工作地点
    :param job_message_source: 消息来源
    :param job_position: 工作职位
    :param job_release_time: 工作发布时间
    :param web_html: 抓取的网页html
    :return:
    """
    if type(job_city) == list:
        job_city = '#'.join(job_city)
    if type(job_position) == list:
        job_position = '#'.join(job_position)
    token = hashlib.md5(job_company.encode("UTF-8")).hexdigest()
    job_release_time = tools.get_real_time(job_release_time)
    sql = """
        insert into jobs(title, company, position, web_url, work_city, message_source, job_type,
        authentication, status, web_html, release_time, token, create_time)
        values(%s, %s, %s, %s, %s, %s, 0, 0, 0, %s, %s, %s, now());
<<<<<<< HEAD
    """
=======
          """
>>>>>>> origin/banana
    try:
        insert_id = db_lib.insert(sql, [job_title, job_company, job_position, job_url, job_city, job_message_source,
                                        web_html, job_release_time, token])
        add_company(job_company)
        return insert_id
    except IntegrityError:
        return 0
    except Exception as error:
        log.error("写入数据库失败（错误类型：%s）， 信息地址：%s" % (str(error), job_url))
        return -1

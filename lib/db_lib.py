# coding:UTF-8


"""
数据库操作简易封装
@author: yubang
2016.02.29
"""

from config import db_config
import pymysql as MySQLdb


def get_db_connection():
    """
    获取新的数据库连接，请注意自己关闭连接
    :return:
    """
    conn = MySQLdb.connect(host=db_config.db_config_data['db_host'], user=db_config.db_config_data['db_user'],
                           passwd=db_config.db_config_data['db_password'], db=db_config.db_config_data['db_name'],
                           port=db_config.db_config_data['db_port'], charset="utf8")
    return conn


def close_db_connection(db_connection):
    """
    关闭数据库连接
    :param db_connection: 数据库连接句柄
    :return:
    """
    db_connection.close()


def query_for_dict(sql, params=None):
    """
    执行数据库查询，返回一个字典，如果没有数据返回None
    :param sql: 原始sql
    :param params: 需要填充的参数列表（字符串自动转椅）
    :return:
    """
    objs = query_for_list(sql, params)
    if objs:
        return objs[0]
    else:
        return None


def query_for_list(sql, params=None):
    """
    执行数据库查询，返回一个列表，如果没有数据返回None
    :param sql: 原始sql
    :param params: 需要填充的参数列表（字符串自动转椅）
    :return:
    """
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    if params is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, params)

    objs = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)
    return objs


def update(sql, params=None):
    """
    执行sql，返回影响行数
    :param sql: 原始sql
    :param params: 需要填充的参数列表（字符串自动转椅）
    :return:
    """

    if params is None:
        params = []

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(sql, params)
    count = cursor.rowcount
    conn.commit()
    cursor.close()
    close_db_connection(conn)
    return count


def insert(sql, params=None):
    """
    执行sql，返回插入后自增id
    :param sql: 原始sql
    :param params: 需要填充的参数列表（字符串自动转椅）
    :return:
    """

    if params is None:
        params = []

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(sql, params)
    table_id = int(cursor.lastrowid)
    conn.commit()

    cursor.close()
    close_db_connection(conn)

    return table_id

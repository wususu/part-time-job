# coding:UTF-8


"""
数据库配置
"""


import os


db_config_data = {
    'db_name': 'work',
    'db_user': 'root',
    'db_password': 'root',
    'db_port': 3306,
    'db_host': '127.0.0.1'
}

if os.environ.get('own_env_name', None) == 'wususu':
    db_config_data = {
        'db_name': 'work',
        'db_user': 'root',
        'db_password': 'root',
        'db_port': 3306,
        'db_host': '127.0.0.1'
    }



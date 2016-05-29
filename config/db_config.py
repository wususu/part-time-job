# coding:UTF-8


"""
数据库配置
"""


import os


db_config_data = {
    'db_name': 'work',
    'db_user': 'work',
    'db_password': 'work2016',
    'db_port': 3306,
    'db_host': '192.168.249.78'
}

#
# if os.environ.get('own_env_name', None) == 'yubang':
#     db_config_data = {
#         'db_name': 'work',
#         'db_user': 'work',
#         'db_password': '',
#     }
# if os.environ.get('own_env_name', None) == 'wususu':
#     db_config_data = {
#         'db_name': 'work',
#         'db_user': 'root',
#         'db_password': 'root',
#     }
# if os.environ.get('own_env_name', None) == 'coffeesign':
#     db_config_data = {
#         'db_name': 'test',
#         'db_user': 'root',
#         'db_password': 'coffeesign',
#         'db_port': 3306,
#         'db_host': '127.0.0.1'
#     }
#
#

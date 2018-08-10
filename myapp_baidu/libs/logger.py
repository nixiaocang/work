# -*- coding:utf-8 -*-

import os
import logging
import logging.config
from myapp_baidu.config.app_config import load_config
version=os.environ.get('ENV', 'Local')
config_obj = load_config(version)
log_path = config_obj.LOG_PATH
if not os.path.exists(log_path):
    os.makedirs(log_path)

pwd = os.path.realpath(__file__)
path = os.path.abspath(os.path.dirname(pwd))
path = os.path.join(path, '../config/logging.conf')
logging.config.fileConfig(path, defaults = {'log_path': log_path})


def sync_logger():
    return logging.getLogger('sync')


def receive_logger():
    return logging.getLogger('receive')


def task_logger():
    return logging.getLogger('task')


def runtime_logger():
    return logging.getLogger('runtime')

def api_logger():
    return  logging.getLogger('api')

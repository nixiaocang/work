#coding:utf-8
import os
import json
import psycopg2
import datetime
import pandas as pd
from sqlalchemy import create_engine
from myapp_baidu.config.app_config import load_config

version = os.environ.get('ENV', 'Local')
config_obj = load_config(version)


class DBModel(object):
    def __init__(self):
        try:
            self.conn = psycopg2.connect(database=config_obj.DATABASE, user=config_obj.USER, password=config_obj.PASSWORD, host=config_obj.HOST, port=config_obj.PORT)
        except Exception as e:
            raise Exception("数据库:%s连接失败" % database)
        self.cursor =self.conn.cursor()

    def update(self, key):
        now = str(datetime.datetime.today())[:19]
        print(now)
        sql = "update public.t_conf set f_data_last_updated_ts=%s where f_email=%s"
        params = (now, key)
        self.cursor.execute(sql, params)
        self.conn.commit()

    def insert(self, data):
        sql = "insert into public.t_conf(f_schema,f_exec_time_of_day,f_email,f_data_last_updated_ts,f_history,f_retry_interval,f_retry_times) values (%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, data)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

def write_data(df, table_name, schema):
    df = pd.read_json(json.dumps(data_list1))
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format({'user':config_obj.USER, 'password':config_obj.PASSWORD, 'host':config_obj.HOST, 'port':config_obj.PORT, 'database':config_obj.DATABASE}))
    try:
        df.to_sql(table_name,engine,index=False,if_exists='append', schema = schema)
    except Exception as e:
        print(e)
        raise e
    return True

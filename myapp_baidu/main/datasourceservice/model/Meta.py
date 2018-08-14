#coding:utf-8
import os
import json
import hashlib
import psycopg2
import datetime
import pandas as pd
from sqlalchemy import create_engine

class DBModel(object):
    def __init__(self, dbinfo):
        self.dbinfo = dbinfo
        try:
            self.conn = psycopg2.connect(database=dbinfo['pt_db_name'], user=dbinfo['pt_db_user'], password=dbinfo['pt_db_pwsd'], host=dbinfo['pt_db_host'], port=dbinfo['pt_db_port'])
        except Exception as e:
            print(e)
            raise Exception("数据库:%s连接失败" % dbinfo['pt_db_name'])
        self.cursor =self.conn.cursor()

    def update_t_conf(self):
        now = str(datetime.datetime.today())[:19]
        sql = "update ptmind.t_conf set f_data_last_updated_ts=%s where f_company_id=%s"
        params = (now, self.dbinfo['pt_company_id'])
        self.cursor.execute(sql, params)
        self.conn.commit()

    def insert(self, data):
        now = str(datetime.datetime.today())[:19]
        bag = {
                'f_task_id':self.dbinfo['f_task_id'],
                'f_email':self.dbinfo['pt_email'],
                'f_company_id':self.dbinfo['pt_company_id'],
                'f_source':self.dbinfo['pt_source'],
                'f_db':get_md5_string(self.dbinfo),
                'f_started_ts':now,
                'f_date':self.dbinfo['pt_data_from_date'],
                }
        bag.update(data)
        if 'f_error_msg' in data.keys():
            bag['f_error_ts'] = now
            sql = "insert into ptmind.t_task_trace(f_task_id,f_email,f_company_id,f_source,f_db,f_table,f_account,f_started_ts,f_error_ts,f_error_msg, f_date) values (%(f_task_id)s,%(f_email)s,%(f_company_id)s,%(f_source)s,%(f_db)s,%(f_table)s,%(f_account)s,%(f_started_ts)s,%(f_error_ts)s, %(f_error_msg)s, %(f_date)s)"
        else:
            sql = "insert into ptmind.t_task_trace(f_task_id,f_email,f_company_id,f_source,f_db,f_table,f_account,f_started_ts, f_date) values (%(f_task_id)s,%(f_email)s,%(f_company_id)s,%(f_source)s,%(f_db)s,%(f_table)s,%(f_account)s,%(f_started_ts)s, %(f_date)s)"
        self.cursor.execute(sql, bag)
        self.conn.commit()

    def update_t_task_trace(self, number):
        now = str(datetime.datetime.today())[:19]
        sql = "update ptmind.t_task_trace set f_ended_ts=%s , f_data_count=%s where f_company_id=%s and f_task_id=%s"
        data = (now, number, self.dbinfo['pt_company_id'], self.dbinfo['f_task_id'])
        self.cursor.execute(sql, data)
        self.conn.commit()


    def __del__(self):
        self.conn.close()

def write_data(df, dbinfo, table_name):
    schema = dbinfo['pt_db_schema']
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**{'user':dbinfo['pt_db_user'], 'password':dbinfo['pt_db_pwsd'], 'host':dbinfo['pt_db_host'], 'port':dbinfo['pt_db_port'], 'database':dbinfo['pt_db_name']}))
    con = engine.connect()
    try:
        df.to_sql(table_name, engine, index=False, if_exists='append', schema=schema)
    except Exception as e:
        print(e)
        raise e
    finally:
        con.close()
        engine.dispose()

    return True

def get_md5_string(dbinfo):
    src = dbinfo['pt_db_host'] + dbinfo['pt_db_name'] + dbinfo['pt_db_user'] + dbinfo['pt_db_pwsd']
    m2 = hashlib.md5()
    m2.update(src.encode("utf8"))
    return m2.hexdigest()


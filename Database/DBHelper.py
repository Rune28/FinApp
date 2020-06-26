# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:33:02 2020

@author: aovch
"""


from configs import config_database as config
import psycopg2
from datetime import datetime


class ConnectionPSQL:
    def __init__(self, 
        host=config.host,
        user=config.user, 
        password=config.password, 
        dbname=config.dbname, 
        port = config.port):
        self.conn = psycopg2.connect(host=host,
                                     user=user, 
                                     password=password, 
                                     dbname=dbname, 
                                     port = port)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        print('Connection inited')

class UserDBHelper(ConnectionPSQL):
    def __init__(self, 
        host=config.host,
        user=config.user, 
        password=config.password, 
        dbname=config.dbname, 
        port = config.port):

        super().__init__(host,user,password,dbname,port)
        self.user_table()
        print('User Table inited')

    def user_table(self):
        table = """
        CREATE TABLE IF NOT EXISTS "Users" 
        ("Id" SERIAL PRIMARY KEY,
        "CreatedOn" timestamp, 
        "Name" varchar(128), 
        "Password" uuid, 
        "Status" int,
        "UserBotId" int,
            "First_name" varchar(255),
            "Last_name" varchar(255),
            "Username" varchar(255))"""
        # index_user = 'Create index'
        try:
            self.cur.execute(table)
        except Exception as e:
            print(e)

    def add_user(self, name,password,bot_id,f_name,l_name,u_name):
        try:
            stmt = """INSERT INTO "Users" ("CreatedOn",
            "Name", 
            "Password", 
            "Status", 
            "UserBotId",
            "First_name",
            "Last_name",
            "Username") VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"""
            args = (datetime.now(),name,password,0,bot_id,f_name,l_name,u_name)
            self.cur.execute(stmt, args)
        except Exception as e:
            print(e)
        # self.conn.commit()

    def delete_user(self, name):
        stmt = """DELETE FROM "Users" WHERE "Name" = (?)"""
        args = (name)
        self.cur.execute(stmt, args)
        # self.conn.commit()
    
    def check_user(self, name):
        qry = f"""Select "Id" from "Users" where "Name" = '{name}'"""
        self.cur.execute(qry)
        if self.cur.fetchone():
            return True
        else:
            return False

    def check_id(self, ids):
        qry = f"""Select "Id" from "Users" where "UserBotId" = '{ids}'"""
        self.cur.execute(qry)
        if self.cur.fetchone():
            return True
        else:
            return False
    
    def login_user(self, name,password):
        try:
            qry = f"""Select "Id" from "Users" where "Name" = '{name}' and "Password" = '{password}'"""
            self.cur.execute(qry)
            if self.cur.fetchone():
                return True
            else:
                return False
        except Exception as e:
            print(e)


class StocksDbHelper(ConnectionPSQL):
    def __init__(self, 
                host=config.host,
                user=config.user, 
                password=config.password, 
                dbname=config.dbname, 
                port = config.port):
        super().__init__(host,user,password,dbname,port)
        self.tickers_table()
        print('Stocks Table inited')
        
    def tickers_table(self):
        table = """
        CREATE TABLE IF NOT EXISTS "Stocks" 
        ("Id" SERIAL PRIMARY KEY,
        "CreatedOn" timestamp DEFAULT now(),
        "Symbol" varchar(20), 
        "Exchange" varchar(20),
        "Name" varchar(128), 
        "DateIex" varchar(10), 
        "Status" boolean,
        "TypeProduct" varchar(6),
            "Region" varchar(255),
            "Currency" varchar(255),
            "iexId" varchar(255)  ,
            "figi" varchar(255) )"""
        # index_user = 'Create index'
        try:
            self.cur.execute(table)
        except Exception as e:
            print(e)

    def get_stocks(self, like_var):
        stmt = f"""SELECT"" "Symbol","Name"
                    FROM "Stocks" 
                    where "Symbol" ~* '{like_var}' or "Name" ~* '{like_var}'"""
        return ['/'.join([x[0],x[1]]) for x in self.conn.execute(stmt)]
    
    def insert_stocks(self,tuples_stocks):
        try:
            stmt = """INSERT INTO "Stocks" (
                    "Symbol",
                    "Exchange",
                    "Name", 
                    "DateIex", 
                    "TypeProduct",
                    "iexId",
                    "Region",
                    "Currency",
                    "Status",
                    "figi") VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s)"""
            self.cur.execute(stmt, tuples_stocks)
        except Exception as e:
            print(e)

finapp_users = UserDBHelper(host=config.host,
                user=config.user, 
                password=config.password, 
                dbname=config.dbname, 
                port = config.port)
finapp_stocks = StocksDbHelper(host=config.host,
                user=config.user, 
                password=config.password, 
                dbname=config.dbname, 
                port = config.port)
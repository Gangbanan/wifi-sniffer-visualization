import sys
sys.path.append('../../')

import psycopg2
from setting import *

def getDBConn():

    # builds the connection string
    str_conn_string = DB_CONN_STRING % (DB_HOST, DB_NAME, DB_USER_NAME, DB_PASSWORD)
	
    return psycopg2.connect(str_conn_string)

def executeQuery(obj_conn, str_query):
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    obj_cursor = obj_conn.cursor()

    # execute our Query
    obj_cursor.execute(str_query)
    
    t_output = obj_cursor.fetchall()

    return t_output

def executeSelect(obj_conn, str_query):
    obj_cursor = obj_conn.cursor()
    # execute our Query
    obj_cursor.execute(str_query)
    obj_conn.commit()

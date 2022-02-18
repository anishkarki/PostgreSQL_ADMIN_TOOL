import psycopg2
import os
from .confighandler import config

def connect(filename, section):
    """Connect to the PostgreSQL database server"""
    try:
        params = config(filename, section)
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        return conn, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query_executer(qyery, cur):
    """Execute a query"""
    try:
        cur.execute(qyery)
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


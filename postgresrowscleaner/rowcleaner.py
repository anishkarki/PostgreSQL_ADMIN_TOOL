from configparser import ConfigParser
from .queryexecuter import connect, query_executer
import os
from .confighandler import config_grabber

current_path=os.path.dirname(os.path.abspath(__file__))
configfile=os.path.join(current_path,'./database.ini')
deletable_row_file = os.path.join(current_path,'./deletable_row_detail.ini')


def change_config(config_file, section, option, value):
    try:
        config = ConfigParser()
        config.read(config_file)
        config.set(section, option, value)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        print(f'Successfully changed value of {option} to {value} in {config_file}.')
    except Exception as e:
        print(e)

def connect_execute(filename=configfile, section="postgresql",query="select version()"):
    try:
        conn, cur = connect(filename, section)
        cur_out = query_executer(query,cur)
        return cur_out
    except Exception as e:
        print(e)

def prepare_query(filename, section):
    tablename=config_grabber(filename, section, 'table_name')
    condition=config_grabber(filename, section, 'condition')
    if tablename is not None and condition is not None:
        count_query=f"select count(*) from {tablename} where {condition}"
        delete_query=f"delete from {tablename} where {condition}"
        return tablename,condition,count_query,delete_query
    else:
        print("Error in config file. Please check the config file. Please add the config with function add_tableconfig_with_condition.")
        return None,None,None,None

def vaccum(cur, tablename):
    old_isolation_level = cur.connection.isolation_level
    cur.connection.set_isolation_level(0)
    cur.execute(f"VACUUM ANALYZE {tablename}")
    cur.connection.set_isolation_level(old_isolation_level)
    return cur


def row_cleaner(filename=configfile, section="postgresql", tablename=None):
    '''
    This function will delete rows from a table based on the condition specified in the config file.
    '''
    try:
        conn, cur = connect(filename, section)
        tablename,condition,count_query,delete_query = prepare_query(deletable_row_file, tablename)
        if all([tablename,condition,count_query,delete_query]):
            cur_out = query_executer(count_query, cur)
            print(f'Total rows to be deleted: {cur_out.fetchone()[0]} rows from {tablename} with condition {condition}.')
            cur_out = query_executer(delete_query, cur)
            print(f'Total rows deleted: {cur_out.rowcount}')
            cur_out = vaccum(cur, tablename)
            print(f'Vaccum done for {tablename}')
            conn.commit()
            return cur_out
        else:
            print("Error in config file. Please check the config file.")
            return None
    except Exception as e:
        print(e)
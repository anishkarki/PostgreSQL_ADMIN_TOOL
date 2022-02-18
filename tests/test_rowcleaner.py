from postgresrowscleaner import rowcleaner, queryexecuter
import psycopg2
import time

def create_dummy_db():
    try:
        conn = psycopg2.connect("dbname='postgres' user='user' host='127.0.0.1' password='admin' port='54320'")
        cur = conn.cursor()
        cur.execute("create table public.historical_claim_responses (id integer, data jsonb, response jsonb);")
        cur.execute("insert into public.historical_claim_responses select i,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) ||'\",\"address\":\"'||md5(random()::text)||'\"}')::jsonb,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) || '\",\"address\":\"' || md5(random()::text)||'\"}')::jsonb from generate_series(1,10000) s(i);")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def test_queryexecuter():
    a = rowcleaner.connect_execute()
    assert "PostgreSQL" in a.fetchall()[0][0]

def test_row_cleaner():
    b = rowcleaner.row_cleaner(tablename="historical_claim_reponses")
    assert "VACUUM" == b.statusmessage


from postgresrowscleaner import rowcleaner
import psycopg2

def create_dummy_db():
    conn = psycopg2.connect(database="postgres", user="user", password="admin",host="localhost")
    cur = conn.cursor()
    cur.execute("create table public.historical_claim_responses (id integer, data jsonb, response jsonb);")
    cur.execute("insert into postgres.public.historical_claim_responses select i,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) ||'\",\"address\":\"'||md5(random()::text)||'\"}')::jsonb,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) || '\",\"address\":\"' || md5(random()::text)||'\"}')::jsonb from generate_series(1,10000) s(i);")
    conn.commit()
    conn.close()

def test_queryexecuter():
    a = rowcleaner.connect_execute()
    assert "PostgreSQL" in a.fetchall()[0][0]

def test_row_cleaner():
    b=rowcleaner.row_cleaner(tablename="dvdrental.public.historical_claim_reponses")
    assert "VACUUM" == b.statusmessage


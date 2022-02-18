from postgresrowscleaner import rowcleaner, queryexecuter
import time


def test_create_dummy_db():
    try:

        rowcleaner.connect_execute(query="create table public.historical_claim_responses (id integer, data jsonb, response jsonb)")
        print("success")
        rowcleaner.connect_execute(query="insert into public.historical_claim_responses select i,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) ||'\",\"address\":\"'||md5(random()::text)||'\"}')::jsonb,('{\"firstName\":\"' ||  md5(random()::text) || '\", \"lastName\":\"' || md5(random()::text) || '\",\"address\":\"' || md5(random()::text)||'\"}')::jsonb from generate_series(1,10000) s(i);")

    except Exception as e:
        print(e)


def test_queryexecuter():
    a = rowcleaner.connect_execute()
    print(a)
    assert "PostgreSQL" in a.fetchall()[0][0]

def test_row_cleaner():
    b = rowcleaner.row_cleaner(tablename="historical_claim_responses")
    assert "VACUUM" == b.statusmessage


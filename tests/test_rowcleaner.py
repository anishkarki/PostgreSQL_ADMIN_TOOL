from postgresrowscleaner import rowcleaner

def test_queryexecuter():
    a = rowcleaner.connect_execute()
    assert "PostgreSQL" in a.fetchall()[0][0]

def test_row_cleaner():
    b=rowcleaner.row_cleaner(tablename="dvdrental.public.historical_claim_reponses")
    assert "VACUUM" == b.statusmessage


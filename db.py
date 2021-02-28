import psycopg2 as pg
from config import HOST, DATABASE, USER, PASSWORD

sql = """
insert into users (username, karma, rank)
select
    '{username}',
    coalesce((select karma from users where username = '{username}'), 1),
    'soldier'
on conflict (username)
do update set karma = EXCLUDED.karma + 1
returning karma;
"""

def increment_karma(username: str) -> int:
    conn_str = "host='%s' dbname='%s' user='%s' password='%s'" % (HOST, DATABASE, USER, PASSWORD)
    with pg.connect(conn_str) as con:
        con.autocommit = True
        cur = con.cursor()
        cur.execute(sql.format(username=username))
        res = cur.fetchall()
        return res[0][0]


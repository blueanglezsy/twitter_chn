import sqlite3 as sqlite
import re

jpn_search = re.compile(ur"[\u3040-\u309F\u30A0-\u30FF]").search
krn_search = re.compile(ur"[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]").search
DATABASE = 'networks_1'
DATABASE_1 = 'networks_1'

def init():
    """docstring for init"""
    con = get_connection()
    cursor = con.cursor()
    create_twitter_user(cursor)
    create_twitter_relation(cursor)
    create_non_chn_user(cursor)
    con.commit()
    cursor.close()

def create_twitter_user(cursor):
    try:
        cursor.execute('''drop table if exists t_user''')
        cursor.execute('''create table t_user 
            (id integer primary key autoincrement,
            user_id integer unique not null,
            user_id_str text unique not null,
            screen_name text not null,
            name text not null,
            foer_cnt integer not null,
            friend_cnt integer not null,
            desc text,
            location text,
            created_at date not null,
            status_cnt integer not null,
            verified integer,
            scanned integer)''')
    except sqlite.InterfaceError:
        print "can't create table t_user"

def create_twitter_relation(cursor):
    try:
        cursor.execute('''drop table if exists t_relation''')
        cursor.execute('''create table t_relation 
            (twitter_user integer, foer integer,
            primary key(twitter_user, foer))''')
    except sqlite.InterfaceError:
        print "can't create talbe t_relation"

def create_non_chn_user(cursor):
    try:
        cursor.execute('''drop table if exists no_chn_twitter''')
        cursor.execute('''create table no_chn_twitter 
            (twitter_id integer)''')
    except sqlite.InterfaceError:
        print "can't create talbe t_relation"

def save_non_chn(id, con=None, cursor=None):
    con = con or get_connection()
    cursor = cursor or con.cursor()
    cursor.execute('''select * from no_chn_twitter where
        twitter_id=?''',(id,))
    if not is_in_no_chn(id):
        cursor.execute('''insert into no_chn_twitter(twitter_id) 
            values (?)''', (id,))
        con.commit()

def is_in_no_chn(id, con=None, cursor=None):
    existen=False
    con = con or get_connection()
    cursor = cursor or con.cursor()
    cursor.execute('''select * from no_chn_twitter where
        twitter_id=?''',(id,))
    if cursor.fetchone():
        existen = True
    else: 
        existen=False
    return existen

def pick_jnp(con=None, cursor=None):
    con = con or get_connection()
    cursor = cursor or con.cursor()
    cursor.execute('''select id, name, desc from t_user''')
    result = cursor.fetchall()
    ids = [row[0] for row in result if \
        row[2] and jpn_search(row[2])]
    for id in ids:
        cursor.execute('''update t_user set scanned = 3 where id
                =?''',(id, ))
    con.commit()

def pick_krn(con=None, cursor=None):
    con = con or get_connection()
    cursor = cursor or con.cursor()
    cursor.execute('''select id, name, desc from t_user''')
    result = cursor.fetchall()
    ids = [row[0] for row in result if \
        row[2] and krn_search(row[2])]
    for id in ids:
        cursor.execute('''update t_user set scanned = 4 where id
                =?''',(id, ))
    con.commit()
        
def get_connection():
    con = sqlite.connect(DATABASE,
        detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    return con

def get_connection_1():
    con = sqlite.connect(DATABASE_1,
        detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    return con

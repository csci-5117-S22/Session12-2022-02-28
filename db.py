""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()


# person table

def create_or_update_user(person_id, person_name, person_picture):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding person %s", person_name)
        cur.execute("""INSERT INTO person (person_id, name, image) 
                                   values (%s, %s, %s)
                        ON CONFLICT (person_id) DO UPDATE SET name=%s, image=%s""", (person_id, person_name, person_picture, person_name, person_picture))

def get_people(page = 0, per_page = 12):
    ''' note -- result can be used as list of dictionaries'''
    limit = per_page
    offset = page*per_page
    with get_db_cursor() as cur:
        cur.execute("select * from person order by person_id limit %s offset %s", (limit, offset))
        return cur.fetchall()

def get_gifts_for_person(person, page = 0, per_page = 12):
    limit = per_page
    offset = page*per_page
    with get_db_cursor() as cur:
        cur.execute("select * from gift_idea where person_id = %s limit %s offset %s", (person, limit, offset))
        return cur.fetchall()

def get_person(person_id):
    with get_db_cursor() as cur:
        cur.execute("select * from person where person_id = %s", (person_id,))
        return cur.fetchone()

def update_description(person_id, description):
    with get_db_cursor(True) as cur:
        cur.execute("update person set description=%s, first_time=False where person_id = %s", (description, person_id))

def add_idea(person_id, name, link):
    with get_db_cursor(True) as cur:
        cur.execute("""INSERT INTO gift_idea (person_id, product, external_link, purchased) 
                                   values (%s, %s, %s, False)""", 
                                   (person_id, name, link))

def update_gift(gift_id, bought):
    with get_db_cursor(True) as cur:
        cur.execute("update gift_idea set purchased=%s where gift_idea_id = %s", (bought, gift_id))

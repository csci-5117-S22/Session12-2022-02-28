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

def add_person (name):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding person %s", name)
        cur.execute("INSERT INTO person (name) values (%s)", (name,))

def get_people(page = 0, people_per_page = 10):
    ''' note -- result can be used as list of dictionaries'''
    limit = people_per_page
    offset = page*people_per_page
    with get_db_cursor() as cur:
        cur.execute("select * from person order by person_id limit %s offset %s", (limit, offset))
        return cur.fetchall()

def get_gifts_for_person(person):
    with get_db_cursor() as cur:
        cur.execute("select product, external_link from gift_idea where person_id = %s", (person,))
        return cur.fetchall()

def get_name_for_person(person):
    with get_db_cursor() as cur:
        cur.execute("select name from person where person_id = %s", (person,))
        return cur.fetchone()['name']

def get_most_popular_gift():
    with get_db_cursor() as cur:
        cur.execute("select product, external_link from gift_idea group by product, external_link order by count(*) desc;")
        return dict(cur.fetchone())



def get_image(img_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM images where image_id=%s", (img_id,))
        return cur.fetchone()

def upload_image(data, filename):
    with get_db_cursor(True) as cur:
        cur.execute("insert into images (filename, data) values (%s, %s)", (filename, data))

def get_image_ids():
    with get_db_cursor() as cur:
        cur.execute("select image_id from images order by image_id desc limit 12 ;")
        return [r['image_id'] for r in cur]
        
        
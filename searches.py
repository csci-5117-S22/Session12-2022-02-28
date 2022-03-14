from dotenv import load_dotenv
import db
import time

# get .env data.    
load_dotenv()
# setup the db
db.setup()

def title_like(search):
    start = time.time()
    with db.get_db_cursor() as cur:
        
        
        search = "%"+search+"%" # % in a "like" acts as a wildcard
        cur.execute("select * from movie where title like %s;", (search,))
        
        
        rowcount = 0
        for row in cur:
            print(row['movieid'], row['title'])
            rowcount += 1
    stop = time.time()
    print("took", stop-start, "seconds and returned", rowcount, "rows")

def synopsis_like(search):
    start = time.time()
    with db.get_db_cursor() as cur:
        
        
        search = "%"+search+"%" # % in a "like" acts as a wildcard
        cur.execute("select * from movie where synopsis like %s;", (search,))
        
        
        rowcount = 0
        for row in cur:
            if (rowcount < 10):
                print(row['movieid'], row['title'])
            rowcount += 1
    stop = time.time()
    print("took", stop-start, "seconds and returned", rowcount, "rows")

def synopsis_full_text(search):
    start = time.time()
    with db.get_db_cursor() as cur:
       
       
        # there are _multiple_ ways to query this, `@@ plainto_tsquery` does an "all words" match
        # you can actually do this with arbitrary boolean complexity if you want by making your own tsqueries.
        # https://www.postgresql.org/docs/9.5/textsearch-controls.html
        cur.execute("select * from movie where search @@ plainto_tsquery('english', %s) order by ts_rank(search, plainto_tsquery('english', %s)) desc;", (search,search))
        
        
        rowcount = 0
        for row in cur:
            if (rowcount < 10):
                print(row['movieid'], row['title'])
            rowcount += 1
    stop = time.time()
    print("took", stop-start, "seconds and returned", rowcount, "rows")

 
search = input("What do you want to search for? ")
# Good examples: batman
# spooky haunting
title_like(search)
input("press enter when ready")
synopsis_like(search)
input("press enter when ready")
synopsis_full_text(search)
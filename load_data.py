from dotenv import load_dotenv
import db
import csv
import random

# get .env data.    
load_dotenv()
# setup the db
db.setup()

# load a random dataset with movie titles and descriptions that I found on keggle:
# https://www.kaggle.com/cryptexcode/mpst-movie-plot-synopses-with-tags
# not _really_ what the data is posted for, but it's fine.
with db.get_db_cursor(True) as cur:
    with open('mpst_full_data.csv') as raw:
        reader = csv.DictReader(raw)
        reader = list(reader)
        random.shuffle(reader)
        for row in reader[:5000]: # just take 5000 movies -- I have a row limit to think about!
            cur.execute("insert into movie (movieid, title, synopsis, search) values (%s, %s, %s, to_tsvector('english', %s));", (row['imdb_id'], row['title'], row['plot_synopsis'], row['plot_synopsis']))


    
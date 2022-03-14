-- code for "deleting" everything -- useful when you plan to nuke-and-page frequently.
drop table if exists gift_idea;
drop table if exists person;

create table person (
  person_id text PRIMARY KEY,
  name text NOT NULL,
  image text NOT NULL,
  description text default 'No Description set yet.',
  first_time boolean default True
);

create table gift_idea (
  gift_idea_id SERIAL PRIMARY KEY,
  person_id text references person,
  product text NOT NULL,
  external_link text,
  purchased boolean
);

drop table if exists movie;

create table movie (
  movieid varchar(256) primary key,
  title text,
  synopsis text,
  search tsvector
);
-- indexes instruct the database about what types of queries you will run
-- this says "I'm going to do full text searches -- plan on it so it's fast"
-- adding this took my search time from about 10 seconds to 0.23 (just filter -- not sorting)
-- you can also explicitly store "term vectors" to speed things up further.
CREATE INDEX movie_search_idx ON movie USING GIN (search);

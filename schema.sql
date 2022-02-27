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

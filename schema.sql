create table person (
  person_id SERIAL PRIMARY KEY,
  name varchar(255) NOT NULL
);

create table gift_idea (
  gift_idea_id SERIAL PRIMARY KEY,
  person_id int references person,
  product text NOT NULL,
  external_link text
);

insert into person (name) values ('Daniel Kluver');

-- A surprising percent of people I interact with each month are named Laura
insert into person (name) values ('Laura (work)');
insert into person (name) values ('Laura (house)');
insert into person (name) values ('Laura (family)');

insert into gift_idea (person_id, product, external_link) values (1, 'Laser cutter', 'https://all3dp.com/1/best-home-desktop-laser-cutter-engraver-aio-machine/');
insert into gift_idea (person_id, product, external_link) values (1, 'Origami Paper', 'https://www.amazon.com/Origami-Paper-Double-Sided-Color/dp/B06XW45PMR');
insert into gift_idea (person_id, product, external_link) values (2, 'Laser cutter', 'https://all3dp.com/1/best-home-desktop-laser-cutter-engraver-aio-machine/');
insert into gift_idea (person_id, product, external_link) values (2, 'metal dice', 'https://diceenvy.com/collections/metal-dice');
insert into gift_idea (person_id, product, external_link) values (3, 'metal dice', 'https://diceenvy.com/collections/metal-dice');
insert into gift_idea (person_id, product, external_link) values (3, 'LOTR first edition', 'https://www.ebay.com/b/1st-Edition-J-R-R-Tolkien-Antiquarian-Collectible-Books/29223/bn_78144267');
insert into gift_idea (person_id, product, external_link) values (4, 'Laser cutter', 'https://all3dp.com/1/best-home-desktop-laser-cutter-engraver-aio-machine/');


-- A table to hold images.
create table images (
  image_id SERIAL PRIMARY KEY,
  filename text,
  data bytea
);

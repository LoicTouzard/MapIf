drop table if exists users;
create table users (
  id integer primary key autoincrement,
  nom text not null,
  prenom text not null,
  email text not null,
  mdp text not null,
  adresse text not null,
  lat real not null,
  lon real not null,
  promo integer not null
);

INSERT INTO users VALUES (0,'bonfante','nicolas','nb@nb.fr','nico','lyon',1.0,2.0,2017);
INSERT INTO users VALUES (1,'touzard','loic','tl@tl.fr','loic','lyon',3.0,4.0,2017);
INSERT INTO users VALUES (2,'lepeigneux','estelle','le@le.fr','estelle','lyon',5.0,6.0,2017);
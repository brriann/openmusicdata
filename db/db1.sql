create database openmusicdata;

create table if not exists artists (
    id serial primary key not null,
    spotifyId varchar(32),
    name varchar(128) not null
);

create table if not exists tracks (
    id serial primary key not null,
    spotifyId varchar(32),
    artistId int not null references artists (id),
    name varchar(128) not null,
    bpm decimal(6,3),
    key int
);

create table if not exists djs (
    id serial primary key not null,
    artistId int unique references artists (id),
    name varchar(128) not null
);

create table if not exists djsets (
    id serial primary key not null,
    djId int not null references djs (id),
    name varchar(128) not null
);

create table if not exists djsettracks (
    id serial primary key not null,
    trackId int not null references tracks (id),
    djSetId int not null references djsets (id),
    ordinal int not null,
    unique (djSetId, ordinal)
);

create index tracks_bpm on tracks (bpm);
create index tracks_key on tracks (key);

insert into artists (spotifyId, name) values ('3LHqODf1hGAgZ5LTw1Gf4C', 'Acid Pauli');
insert into artists (spotifyId, name) values ('5a0etAzO5V26gvlbmHzT9W', 'Nicolas Jaar');
insert into artists (spotifyId, name) values ('6V4bkdqHvsJ2lqkIl4qnG7', 'Birds of Mind');
insert into artists (spotifyId, name) values ('1tRBmMtER4fGrzrt8O9VpS', 'Hot Since 82');

insert into tracks (
    spotifyId, 
    artistId, 
    name, 
    bpm, 
    key
) values (
    '4QHKR48C18rwlpSYW6rH7p', 
    2, 
    'Mi Mujer', 
    124.005, 
    10
);

insert into tracks (
    spotifyId, 
    artistId, 
    name, 
    bpm, 
    key
) values (
    '0YQznyH9mJn6UTwWFHqy4b', 
    2, 
    'El Bandido', 
    124.009, 
    1
);

insert into tracks (
    spotifyId, 
    artistId, 
    name, 
    bpm, 
    key
) values (
    '798mI116dJdZ12n9CkdflI', 
    2, 
    'Time for Us', 
    113.995, 
    4
);

insert into tracks (
    spotifyId, 
    artistId, 
    name, 
    bpm, 
    key
) values (
    '3i8PWTx08WL1vjQYLaX3Fv', 
    2, 
    'Variations', 
    108.372, 
    1
);

explain select * from artists where name = 'Acid Pauli'

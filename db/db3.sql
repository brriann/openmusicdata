-- on-the-go work, porting data/2022_12_21_xyz files into laptop
-- non-serial id => ability to insert PK's and use relations table

create table if not exists artists (
    id int primary key not null,
    spotifyId varchar(32),
    name varchar(128) not null
);

create index artists_spotifyId on artists (spotifyId);

alter table artists add column highlighted boolean not null default false;

create table if not exists artistrelations (
    id int primary key not null,
    sourceArtistId int not null,
    targetArtistId int not null,
    constraint fk_artistrelations_artists_source
        foreign key (sourceArtistId)
        references artists (id)
);

alter table artistrelations
    add constraint fk_artistrelations_artists_target
        foreign key (targetArtistId)
        references artists (id);

create table if not exists queriesrelatedartist (
    id serial primary key not null,
    seedArtistId int not null references artists (id),
    artistsSaved int not null default 0,
    relationsSaved int not null default 0
);

-- after inserting artists with PKs, (with corresponding artistrelation records based on PK)
-- want to have serial/series behavior of PK artist table

-- artists table
CREATE SEQUENCE artists_seq;
ALTER TABLE public.artists ALTER COLUMN id SET DEFAULT nextval('artists_seq');
ALTER TABLE public.artists ALTER COLUMN id SET NOT NULL;
ALTER SEQUENCE artists_seq OWNED BY public.artists.id;    -- 8.2 or later

SELECT MAX(id) FROM public.artists;
SELECT setval('artists_seq', 5);  -- replace 5 by SELECT MAX result

-- artistrelations table
CREATE SEQUENCE artist_relations_seq;
ALTER TABLE public.artistrelations ALTER COLUMN id SET DEFAULT nextval('artist_relations_seq');
ALTER TABLE public.artistrelations ALTER COLUMN id SET NOT NULL;
ALTER SEQUENCE artist_relations_seq OWNED BY public.artistrelations.id;    -- 8.2 or later

SELECT MAX(id) FROM public.artistrelations;
SELECT setval('artist_relations_seq', 5);  -- replace 5 by SELECT MAX result
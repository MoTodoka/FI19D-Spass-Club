PRAGMA encoding = 'UTF-8';

create table activity
(
    uid  INTEGER
        primary key autoincrement,
    name TEXT not null
);

create table location
(
    uid  INTEGER
        primary key autoincrement,
    name TEXT not null
);

create table event
(
    uid       INTEGER
        primary key autoincrement,
    name      TEXT      not null,
    location  INTEGER   not null
        references location,
    timestamp TIMESTAMP not null
);

create table match
(
    uid       INTEGER
        primary key autoincrement,
    timestamp TIMESTAMP not null,
    activity  INTEGER   not null
        references activity,
    location  INTEGER   not null
        references location,
    event     INTEGER
        references event
);

create table player
(
    uid        INTEGER
        primary key autoincrement,
    name       TEXT not null
);

create table score
(
    uid       INTEGER
        primary key autoincrement,
    match     INTEGER not null
        references match,
    player    INTEGER not null
        references player,
    timestamp TIMESTAMP,
    score     INTEGER
);



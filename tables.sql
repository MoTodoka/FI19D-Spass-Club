PRAGMA encoding = 'UTF-8';
PRAGMA foreign_keys = ON;

create table activity
(
    uid  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

create table location
(
    uid  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

create table event
(
    uid       INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT      NOT NULL,
    location  INTEGER   NOT NULL REFERENCES location ON DELETE RESTRICT,
    timestamp TIMESTAMP NOT NULL
);

create table match
(
    uid       INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    activity  INTEGER   NOT NULL REFERENCES activity ON DELETE RESTRICT,
    location  INTEGER   NOT NULL REFERENCES location ON DELETE RESTRICT,
    event     INTEGER REFERENCES event
);

create table player
(
    uid  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

create table score
(
    uid       INTEGER PRIMARY KEY AUTOINCREMENT,
    match     INTEGER NOT NULL REFERENCES match ON DELETE RESTRICT,
    player    INTEGER NOT NULL REFERENCES player ON DELETE RESTRICT,
    timestamp TIMESTAMP,
    score     INTEGER
);



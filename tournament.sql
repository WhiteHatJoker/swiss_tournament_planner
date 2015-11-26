-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players (
	id serial PRIMARY KEY,
	name text,
	wins integer,
	matches integer
);

CREATE TABLE matches (
	id serial PRIMARY KEY,
	winner integer REFERENCES players(id),
	looser integer REFERENCES players(id)
);

--Introducing the row number to every player sorted by his wins record
CREATE VIEW sortedpl AS 
	SELECT id, name, ROW_NUMBER() OVER (ORDER BY wins DESC) as rn FROM players ORDER BY wins DESC;
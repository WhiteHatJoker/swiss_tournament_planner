#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
import psycopg2
from random import randint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) as num from sortedpl;")
    result = c.fetchone()
    DB.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name, wins, matches) VALUES(%s, %s, %s)", (name, 0, 0,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM sortedpl")
    results = c.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner, looser) VALUES(%s, %s)", (winner, loser,))
    c.execute("UPDATE players SET matches=matches+1, wins= wins+1 WHERE players.id=%s", (winner,))
    c.execute("UPDATE players SET matches=matches+1 WHERE players.id=%s", (loser,))
    DB.commit()
    DB.close()

def oddPlayer():
    """Add-on for swissPairings function, which randomly gives a bye to one player if there are odd number of players. In addition,
    it makes sure to give player a bye only once.
    """
    count = countPlayers()
    randnum = randint(1, count)
    byeplayers = []
    oddpairs = []
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id FROM sortedpl WHERE rn=%s LIMIT 1", (randnum,))
    result=c.fetchone()[0]
    if result not in byeplayers:
        byeplayers.append(result)
        byeplayer=result
        c.execute("UPDATE players SET matches=matches+1, wins= wins+1 WHERE players.id=%s", (byeplayer,))
        DB.commit()
        for i in range(0, count-1, 2):
            c.execute("SELECT id, name FROM (SELECT id, name, ROW_NUMBER() OVER (ORDER BY wins DESC) as rn FROM (SELECT * FROM players WHERE NOT (id=ANY(%s))) as newlist ORDER BY wins DESC) as newsortlist WHERE rn>%s LIMIT 2", (byeplayers, i,))
            players = c.fetchall()
            oddpairs.append((players[0][0], players[0][1], players[1][0], players[1][1]))
        DB.close()
        return oddpairs
    else:
        oddPlayer() 
    


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    count = countPlayers()
    pairs = []
    if count%2==0:
        DB = connect()
        c = DB.cursor()
        for i in range(0, count, 2):
            c.execute("SELECT id, name FROM rankedpl WHERE rn>%s LIMIT 2", (i,))
            players = c.fetchall()
            pairs.append((players[0][0], players[0][1], players[1][0], players[1][1]))
        DB.close()
        return pairs
    else:
        oddPlayer()  
    

       

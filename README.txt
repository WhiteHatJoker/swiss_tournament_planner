Swiss Tournament Planner.
=====================

This application is a database scheme that is developed using Python DB-API and PostgreSQL.
The primary purpose of this database is to store the matches between the players, rank players and pair them accordingly.

The zip folder contains the following files.
============================================
1 - tournament.sql
    The database file that contains table and view definitions of our primary database.

2 - tournament.py
    The primary file that contains all the neccessary functions to connect to the database, delete matches, delete players, count players, register players, output standings, record match results and pair up the players.

3 - tournament_test.py
    The file tournament_test.py contains unit tests that will test the functions you’ve written in tournament.py. You can run the tests from the command line, using the command python tournament_test.py.

4 - README.txt

How to run the app.
===================
- Install Vagrant and VirtualBox
- First, fork the fullstack-nanodegree-vm repository so that you have a version of your own within your Github account.
- Next clone your fullstack-nanodegree-vm repo to your local machine.
- To use the Vagrant virtual machine, cd into the full-stack-nanodegree-vm/tournament directory in the terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh (logs into the virtual machine). 
- Remember, once you have executed the vagrant ssh command, you will want to cd /vagrant to change directory to the synced folders in order to work on your project, once your cd /vagrant, if you type ls on the command line, you'll see your tournament folder.
- The Vagrant VM provided in the fullstack repo already has PostgreSQL server installed, as well as the psql command line interface (CLI), so you'll need to have your VM on and be logged into it to run your database configuration file (tournament.sql), and test your Python file with tournament_test.py.
You can need to write psql in terminal to be able to work with the databases interactively in the command line. Next, we need to import the table definitions from tournament.sql by typing \i tournament.sql and then \q to exit psql command line interface.
- Type in python tournament_test.py to see the results of the unit tests.

Functions of tournament.py.
===================

- registerPlayer(name)

Adds a player to the tournament by putting an entry in the database. The database should assign an ID number to the player. Different players may have the same names but will receive different ID numbers.


- countPlayers()

Returns the number of currently registered players. This function should not use the Python len() function; it should have the database count the players.


- deletePlayers()

Clear out all the player records from the database.


- reportMatch(winner, loser)

Stores the outcome of a single match between two players in the database.


- deleteMatches()

Clear out all the match records from the database.


- oddPlayers()

Gives a bye to one player if there are odd number of players


- playerStandings()

Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.


- swissPairings()
Pairs up players with the relatively same number of points.

Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.
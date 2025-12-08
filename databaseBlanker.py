#this one will use sqlite because i am NOT setting up a server for this 
#could use mySQL in the future if we want proper scoreboard implementation
import sqlite3 as sql

batadase = sql.connect("highscores.db")
curse = batadase.cursor()
curse.execute("DROP TABLE IF EXISTS SCORES")

tableQ = """
    CREATE TABLE SCORES (
        placement INT PRIMARY KEY,
        score INT,
        name CHAR(5) NOT NULL,
        unixTime INT
    );
"""

curse.execute(tableQ)
print("wahoo")
curse.close()
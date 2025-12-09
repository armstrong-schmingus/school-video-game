#this one will use sqlite because i am NOT setting up a server for this 
#could use mySQL in the future if we want proper scoreboard implementation
import sqlite3 as sql

batadase = sql.connect("highscores.db")
curse = batadase.cursor()
curse.execute("DROP TABLE IF EXISTS SCORES")

tableQ = """
    CREATE TABLE SCORES (
        id INT  PRIMARY KEY AUTOINCREMENT,
        score INT,
        name CHAR(5) NOT NULL,
        datetime DATETIME DEFAULT CURRENT_TIMESTAMP
    );
"""

def addBlanks():
    curse.execute(tableQ)

    blanky = "('0', '1', 'BLANK', '0')"

    for i in range(50):
        res = blanky[:2] + i + blanky[3:]
        print(res)

#addBlanks()

print("wahoo")
curse.close()
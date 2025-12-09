import sqlite3 as sql
import sys

batadase = sql.connect("highscores.db")
curse = batadase.cursor()

scorey = sys.argv[1] #score
entry = sys.argv[2] #name

addArgument = f"INSERT INTO scores (score, name) VALUES({scorey}, '{entry}');"
removeArgument = "DELETE FROM scores WHERE MIN(score);"

curse.execute(addArgument)

if int(curse.execute("SELECT COUNT(*) FROM scores;")) >100:
    curse.execute(removeArgument)


curse.commit()
curse.close()
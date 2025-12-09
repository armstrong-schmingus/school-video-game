import sqlite3 as sql
import sys

batadase = sql.connect("highscores.db")
curse = batadase.cursor()

scorey = sys.argv[1] #score
entry = sys.argv[2] #name

argument = f"INSERT INTO scores (score, name) VALUES({scorey}, {entry})"
curse.execute(argument)

curse.commit()
curse.close()
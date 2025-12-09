import sqlite3 as sql 

batadase = sql.connect("highscores.db")
curse = batadase.cursor()

argument = "SELECT * FROM scores ORDER BY score ASC;"

curse.execute(argument)

for row in curse.fetchall():
    print(row)
    if row == 10:
        break

curse.close()
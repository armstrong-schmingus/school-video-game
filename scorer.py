import tkinter as tk
import sys, csv, datetime

# Retrieve arguments passed from the calling script
scorey = int(sys.argv[1]) #score
entry = sys.argv[2] #name

class Table:
    def __init__(self,main):
        
        for i in range(total_rows):
            for j in range(total_columns):
                
                self.e = tk.Text(main, width=20,height=1, fg='white', font=('Arial',16,'bold'))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, oldScores[i][j])
                self.e.config(state=tk.DISABLED)

with open("Python/targetPractice/highscores.csv", mode="r") as scores:
        eScores = csv.reader(scores)
        oldScores = []
        for line in eScores:
            oldScores.append(line)

def checkHigh(score):
    with open("Python/targetPractice/highscores.csv", mode="r") as scores:
        eScores = csv.reader(scores)
        next(eScores)
        oldScores = []
        for line in eScores:
            oldScores.append(int(line[0]))
        for i in range(len(oldScores)):
            if oldScores[i] < score:
                return i+1
            elif oldScores[i] == score:
                return i+2
        return "loser"

typey = checkHigh(scorey)

total_rows = len(oldScores)
total_columns = len(oldScores[0])

main = tk.Tk()
main.title('Highscores')

t= Table(main)

def fetchTime():
    time = str(datetime.datetime.now())
    date = time.rsplit(" ")[0].replace("-", ".")
    time = time.rsplit(" ")[1].rsplit(".")[0]
    times = [time.rsplit(":")[0],time.rsplit(":")[1]]
    time = "".join(times)
    return [date, time]

def buttonClick():
    global oldScores,t,main
    date, time = fetchTime()
    highScore = [scorey, entry, date, time]
    oldScores.insert(typey, highScore)
    oldScores.pop(len(oldScores)-1)

    main.destroy()
    main = tk.Tk()
    main.title('Highscores')

    t= Table(main)

    main.attributes('-topmost',True)
    main.mainloop()

    updateTable(oldScores)

def updateTable(scoreTime):
    r = scoreTime
    with open("Python/targetPractice/highscores.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(r)


if typey != "loser":
    buttonClick()
    total_rows = len(oldScores)
    total_columns = len(oldScores[0])

    main.attributes('-topmost',True)
    main.mainloop()

else:
    tk.Label(main, text=f'Score: {scorey}').grid(row=0,column=1)
    main.attributes('-topmost',True)
    main.mainloop()
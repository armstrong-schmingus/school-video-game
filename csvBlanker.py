import csv

# Field names
f = ['Score', 'Name', 'Date', 'Time']

# nice blank data
blanky = ['0', 'BLANK', '1970.01.01', '0000']
r = []

for i in range(50):
    r.append(blanky)

file = "highscores.csv"

# Writing to CSV file
with open(file, 'w', newline='') as csvfile:
    # Creating a CSV writer object
    csvwriter = csv.writer(csvfile)
    
    # Writing the field names
    csvwriter.writerow(f)
    
    # Writing the data rows
    csvwriter.writerows(r)
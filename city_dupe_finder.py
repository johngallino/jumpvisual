### This program will scan the DB for repeat town names, such as Washington Township, of which there are four of in NJ

import sqlite3

conn = sqlite3.connect('jump.db')
c = conn.cursor()

targetState = "NJ"

c.execute("SELECT city, id FROM UScities WHERE state_id=?", (targetState,))
allTowns = c.fetchall()

print(allTowns)

#class Town:
#    def __init__(self, name, idcode):
#        self.n = name
#        self.i = idcode
#        dupe = false

dupeTowns = []
for town in allTowns:
    target = town[0]
    #print("target is " + town[0])
    count = 0
    for town in allTowns:
        if town[0] == target:
            count += 1
    if count > 1:
        print(target + " appears " + str(count) + " times.")
        dupeTowns.append(target)
        
print(set(dupeTowns))
total = 0
for town in allTowns:
    if town[0] in dupeTowns:
        c.execute("UPDATE UScities SET many = 1 WHERE id = ? AND state_id = ?",(town[1], targetState))
        total +=1
    else:
        c.execute("UPDATE UScities SET many = 0 WHERE id = ? AND state_id = ?",(town[1], targetState))
print("found " + str(len(set(dupeTowns))) + " repeat town names in " + targetState)
conn.commit()
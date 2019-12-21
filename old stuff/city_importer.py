import sqlite3
import csv

conn = sqlite3.connect('jump.db')

c = conn.cursor()


# c.execute("""CREATE TABLE UScities (
#             city text,
#             state_id text,
#             state_name text,
#             county_name text,
#             lat real,
#             lng real,
#             zips text,
#             id int

#        ) """)

with open('ctcities.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	next(csv_reader) #this skips the first line of the csv with column names

	for line in csv_reader:
		c.execute("INSERT INTO UScities VALUES (?,?,?,?,?,?,?,?)",(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]))

# c.execute("SELECT * FROM UScities")
# print(c.fetchall())


conn.commit()

conn.close()
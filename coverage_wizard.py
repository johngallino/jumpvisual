import sqlite3
import tkinter as tk


def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
	'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')

conn = sqlite3.connect('jump.db')
c = conn.cursor()

introtext="""This simple program is intended for JumpVisual staff photographers. It will help you choose the towns that you want (or do not want) to cover, and generate a report at the end to input into our database.\n\nLet's get started..."""


root = tk.Tk()
center_window(500, 400)
tk.Label(root, text="Welcome to the JumpVisual Coverage Wizard!", padx=15, pady=15).pack()
tk.Label(root, text=introtext, width=50, wraplength=350, padx=15, pady=15, justify=tk.LEFT).pack()
tk.Button(root, text="Next >>").pack()
tk.Button(root, text="Quit", command=root.destroy).pack()

root.mainloop()
exit()
# name = input("First, please enter your first and last name:\n")

# states_covered = []

# yesno = input("Do you cover any parts of NEW JERSEY? (y/n)")
# while lower(yesno) != 'y' && lower(yesno) != 'n':
# 	yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
# 	states_covered.append('NJ')

# yesno = input("Do you cover any parts of NEW YORK? (y/n)")
# while lower(yesno) != 'y' && lower(yesno) != 'n':
# 	yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
# 	states_covered.append('NY')

# yesno = input("Do you cover any parts of CONNECTICUT? (y/n)")
# while lower(yesno) != 'y' && lower(yesno) != 'n':
# 	yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
# 	states_covered.append('CT')

states = input("Please enter the states that you cover, separated by spaces\n\t(e.g. nj ny ct)\n\n")
states = states.upper()
states = states.split()

for state in states:
	print("\n\nThe counties in " + state + " are...\n")
	c.execute("SELECT county_name FROM UScities WHERE state_id=?", (state,))
	holder = [tup[0] for tup in c.fetchall()]
	counties = []
	for county in holder:
		if county not in counties:
			counties.append(county)		
	counties.sort()
	for county in counties:
		print(county)
	print("===========================")
	counties_covered = input("Please enter every county that you cover partially or completely (separated by spaces)\n")
	counties_covered = counties_covered.upper()
	counties_covered = counties_covered.split()
	print("The counties you cover at least partially are...\n")
	for county in counties_covered:
		print(county + "   ")
	yesno = input("\nIs this correct?")



conn.close()

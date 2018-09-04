import sqlite3

atlantic = ('Absecon',
		'Atlantic City',
		'Brigantine',
		'Buena',
		'Buena Vista Township',
		'Corbin City',
		'Egg Harbor City',
		'Egg Harbor Township',
		'Estell Manor',
		'Folsom',
		'Galloway Township',
		'Hamilton Township',
		'Hammonton',
		'Linwood',
		'Longport',
		'Margate City',
		'Mullica Township',
		'Northfield',
		'Pleasantville',
		'Port Republic',
		'Somers Point',
		'Ventnor City',
		'Weymouth Township')

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
	'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')

# bergen = ['Allendale',
# 'Alpine',
# 'Bergenfield',
# 'Bogota',
# 'Carlstadt',
# 'Cliffside Park',
# 'Closter',
# 'Cresskill',
# 'Demarest',
# 'Dumont',
# 'East Rutherford',
# 'Edgewater',
# 'Elmwood Park',
# 'Emerson',
# 'Englewood',
# 'Englewood Cliffs',
# 'Fair Lawn',
# 'Fairview',
# 'Fort Lee,
# 'Franklin Lakes,
# 'Garfield,
# 'Glen Rock,
# 'Hackensack,
# 'Harrington Park,
# 'Hasbrouck Heights,
# 'Haworth,
# 'Hillsdale,
# 'Ho-Ho-Kus,
# 'Leonia,
# 'Little Ferry,
# 'Lodi,
# 'Lyndhurst,
# 'Mahwah,
# 'Maywood,
# 'Midland Park,
# 'Montvale,
# 'Moonachie,
# 'New Milford,
# 'North Arlington,
# 'Northvale,
# 'Norwood,
# 'Oakland,
# 'Old Tappan,
# 'Oradell,
# 'Palisades Park,
# 'Paramus,
# 'Park Ridge,
# 'Ramsey,
# 'Ridgefield,
# 'Ridgefield Park,
# 'Ridgewood,
# 'River Edge,
# 'River Vale,
# 'Rochelle Park,
# 'Rockleigh,
# 'Rutherford,
# 'Saddle Brook,
# 'Saddle River,
# 'South Hackensack,
# 'Teaneck,
# 'Tenafly,
# 'Teterboro,
# 'Upper Saddle River,
# 'Waldwick,
# 'Wallington,
# 'Washington Township,
# 'Westwood,
# 'Wood-Ridge,
# 'Woodcliff Lake,
# 'Wyckoff
# ]

conn = sqlite3.connect('jump.db')

c = conn.cursor()

print("Welcome to the JumpVisual Coverage Wizard! This simple program will collect the towns that you cover to enter into our system. Let's get started...\n\n")

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

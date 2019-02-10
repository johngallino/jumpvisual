import os
from datetime import date
import shutil

found = os.path.isfile('jump.db')
path = 'backups'
path2 = os.path.join(path, 'jump.db')
today = str(date.today())
LIMIT = 30 #number of backup files to store

if os.path.exists('backups'):
	gix = os.listdir('backups') # dir is your directory path
	number_files = len(gix)

	gix = gix[:number_files-LIMIT]

	for file in gix:
		os.remove('backups/'+file)

if found and not os.path.exists('backups/backup_' + today + '.db'):
	if not os.path.exists('backups'):
		os.mkdir(path, 0o777)
		print("backups folder created")
	shutil.copy2('jump.db', path2)
	os.rename('backups/jump.db', ('backups/backup_' + today + '.db' ))
	print("Made a backup jump.db for today in backups folder")
else:
	print("A backup of jump.db has already been made for today")
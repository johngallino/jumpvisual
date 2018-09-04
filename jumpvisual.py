# import pickle
import sqlite3

from photographer import Photographer

def add_photographer(fname, lname):
    """Creates new photographer object from class and adds it to list of photographers"""
    new_guy = Photographer(fname, lname)
    # photographers.append(new_guy)
    return new_guy

def list_photographers():
    """Displays all photographers in the photographer list"""
    i = 1
    print("\n    PHOTOGRAPHER LIST\n    =================")
    c.execute("SELECT * FROM photographers")
    all_rows = c.fetchall()
    line = ''
    for record in all_rows:
        print('\t' + str(i) + '.  ' + str(record[0]) + ' ' + str(record[1]))
        i+=1
    print('\n')

    choice=input("Enter a number to see details or press Enter to return to the main menu...\n\n\n")
    if int(choice) > 0 and int(choice) <= len(all_rows):
        choice = int(choice) - 1
        print("Profile of: " + str(all_rows[choice][0]) + ' ' + str(all_rows[choice][1]))
        input("Press enter to return to main menu")
    displayMenu()
    
def displayMenu():
    """Displays main menu"""
    menu = ("""\n    MAIN MENU
    ==============
    1. Search a City, State
    2. View photographer list
    3. Add a Photographer
    4. Remove a Photographer
    5. Quit\n""")

    print(menu)
    choice = input("What do you want to do? ")
    while True:
        try:
            choice = int(choice)
            break
        except ValueError:
            choice = input("Not a valid entry! Try again: ")
    #input validation
    while choice < 1 or choice > 5:
        choice = int(input("Not a valid entry. Please try again: "))

    if choice == 1:
        #Search for city, state
        print("\nThat feature has not been implemented yet.")
        input("Press Enter to return to the main menu...\n\n\n")
        displayMenu()
        
    if choice == 2:
        #View photographer list
        list_photographers()
            
    if choice == 3:
        #Add a photographer
        fname = input("\nFirst name: ")
        lname = input("Last name: ")
        new_guy = add_photographer(fname, lname)
        print("\nGreat! " + new_guy.full_name + " has been added to your photographer list. Let's complete their profile...")

        new_guy.fill_profile()
        
        print("\nSo far so good! Here is your new photographer's complete profile...\n")
        print(new_guy.get_profile())
        filename = 'photographers.dat'
        with open(filename, 'wb') as f_obj:
            pickle.dump(photographers, f_obj)
        input("\nPress Enter to return to the main menu...\n\n\n")
        displayMenu()
        
    if choice == 4:
        # Remove a photographer
        list_photographers()
        print("\n")
        edit = input("Who do you want to remove? Or enter 'm' to cancel: ")
        while True:
            while edit.isnumeric():
                edit = int(edit)
                if  int(edit) > 0 and int(edit) <= len(photographers):
                    yesno = input("Are you sure you want to delete " + photographers[edit-1].full_name + "?: ")
                    while yesno != 'y' and yesno != 'n': 
                        yesno = input("Not a valid response. Please enter y or n: ")
                    if yesno == 'y' or yesno == 'Y':
                        rip = photographers[edit-1].full_name
                        del photographers[edit-1]
                        filename = 'photographers.dat'
                        with open(filename, 'wb') as f_obj:
                            pickle.dump(photographers, f_obj)
                        print(rip + " has been deleted. Press Enter to return to main menu.")
                        input()
                        displayMenu()
                    if yesno == 'n' or yesno == 'N':
                        list_photographers()
                        print("\n")
                        edit = input("Who do you want to remove? Or enter 'm' to cancel: ")
                        continue
                    
                    displayMenu()
                else:
                    edit = input("Not a valid attribute. Please try again: ")        
            if edit.isnumeric() == False and edit == 'm':
                print("\n")
                displayMenu()
            else:
                edit = input("uh oh: ")

    if choice == 5:
        # quit the program
        conn.close()
        exit()
        

# LETS START THE FUCKING PROGRAM

filename = 'jump.db'

try:
    with open(filename, 'r'):
        conn = sqlite3.connect('jump.db')
except FileNotFoundError:
    print("Uh oh! " + filename + " is missing!")
except EOFError:
    pass
else:
    print("\nWelcome! Database found...\n")



# conn = sqlite3.connect(':memory:')

c = conn.cursor()

# c.execute("""CREATE TABLE photographers (
#             first text,
#             last text,
#             phone text,
#             email text,
#             slack text,
#             address text,
#             city text,
#             state text,
#             abilities text

#        ) """)

# c.execute("""CREATE TABLE cities (
#             id integer,
#             name text,
#             county text,
#             state text

#        ) """)

# c.execute("""INSERT INTO photographers VALUES (
#         'John', 
#         'Gallino',
#         '201.647.9161',
#         'johngallino@gmail.com',
#         '@gallino',
#         '14 Robin Ln',
#         'Ringwood',
#         'NJ',
#         'P/V/As/Av/Fl'
#         )""")

# c.execute("""INSERT INTO photographers VALUES (

#         'Bob', 
#         'Loblaw',
#         '555-555-5555',
#         'bob@loblawlaw.com',
#         '@boblaw',
#         '100 fake dr',
#         'Emerson',
#         'NJ',
#         'P/V/Fl'

#         )""")




conn.commit()
displayMenu()
conn.close()


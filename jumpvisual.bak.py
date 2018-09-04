import pickle
import sqlite3

from photographer import Photographer

def add_photographer(fname, lname):
    """Creates new photographer object from class and adds it to list of photographers"""
    new_guy = Photographer(fname, lname)
    photographers.append(new_guy)
    filename = 'photographers.dat'
    with open(filename, 'wb') as f_obj:
        pickle.dump(photographers, f_obj)
    return new_guy

def list_photographers():
    """Displays all photographers in the photographer list"""
    i = 1
    print("\n    PHOTOGRAPHER LIST\n    =================")
    for dude in photographers:
        print("    " + str(i) + '. ' + dude.fname.title() + ' ' + dude.lname.title())
        i += 1  
    
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
        if len(photographers) > 0:
            list_photographers()
            
            while True:
                index = input("\nEnter a number to view and/or edit the photographer's full profile,\nor Enter 'm' to return to the main menu: ")
                if index.isnumeric() == False:
                    if index == 'm':
                        displayMenu()
                    else:
                        continue
                if index.isnumeric() == True:
                    # if number corresponds to existing photographer, show photographer profile
                    # else 'display not a valid entry'
                    if int(index) > 0 and int(index) <= len(photographers):
                        print("\n" + photographers[int(index)-1].get_profile())
                        yesno = input("\nWould you like to make an edit? (y/n): ")
                        #input validation
                        while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
                            yesno = input("Not a valid response. Please enter y or n: ")

                        if yesno == 'y' or yesno == 'Y':
                            print("\n" + photographers[int(index)-1].get_profile_to_edit())
                            attribute = input("\nWhat attribute would you like to change? Or enter 'm' to cancel: ")
                            if attribute == 'm':
                                list_photographers()
                                input("\nOkay. Press Enter to return to Photographer list...\n")
                            else:
                                while int(attribute) < 0 or int(attribute) > 9:
                                    attribute = input("Not a valid attribute. Please pick from 1-9: ")
                                photographers[int(index)-1].edit_profile(attribute)
                                filename = 'photographers.dat'
                                with open(filename, 'wb') as f_obj:
                                    pickle.dump(photographers, f_obj)
                                displayMenu()

                        if yesno == 'n' or yesno == 'N':
                            input("\nOkay. Press Enter to return to Photographer list...\n")
                            list_photographers()
                            continue
                    else:
                        continue
                else:
                    continue

        else:
            print("\nYour photographers list is empty!")
            yesno = input("Add a photographer now? (y/n): ")
            if yesno == 'y':
                fname = input("\nFirst name: ")
                lname = input("Last name: ")
                new_guy = add_photographer(fname, lname)
                print("\nGreat! " + new_guy.full_name + " has been added to your photographer list.\nLet's complete their profile...")

                new_guy.fill_profile()
            else:
                print("\n\n\n")
                displayMenu()
            
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
        exit()
        

# LETS START THE FUCKING PROGRAM

filename = 'photographers.dat'
try:
    with open(filename, 'rb') as f_obj:
        photographers = pickle.load(f_obj)
except FileNotFoundError:
    photographers = []
    print("Welcome! No team file found...")
except EOFError:
    pass
else:
    print("\nWelcome! Team file found...\n")


conn = sqlite3.connect('jump.db')
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


c.execute("SELECT * FROM photographers")

print(c.fetchall())

conn.commit()

conn.close()

#displayMenu()
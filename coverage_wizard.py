##import sqlite3
import tkinter as tk
from tkinter import ttk

version = "v1.0"




### FIRST SCREEN
class Frame1(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "Welcome to the JumpVisual Coverage Wizard!"

        self.top_string = ("This simple program is intended for JumpVisual staff photographers. It will help you "
                        "choose the towns that you want (or do not want) to cover, and "
                        "generate a report at the end to input into our database."
                        "\n\nLet's get started!")

        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = ttk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)


        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)




### SECOND SCREEN
class Frame2(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 1"
        self.top_string = ("Enter your name and the states you cover")
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=600)
        self.top_string_label = ttk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=600)
        tk.Label(self, text="First:").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self, text="Last:").grid(row=2, column=1, sticky=tk.W)
        self.f = tk.StringVar()
        self.l = tk.StringVar()
        self.fname_entry = tk.Entry(self, textvariable=self.f)
        self.lname_entry = tk.Entry(self, textvariable=self.l)
        states = tk.Frame(self, pady=20)
        states.grid(row=4, column=0, sticky=tk.W)
        
        tk.Checkbutton(states, text='NJ').grid(row=0, column=0, sticky=tk.W)
        tk.Checkbutton(states, text='NY').grid(row=1, column=0, sticky=tk.W)
        tk.Checkbutton(states, text='CT').grid(row=2, column=0, sticky=tk.W)

        #placing the widgets inside Frame2
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)
        self.fname_entry.grid(row=3, column=0, sticky=tk.W)
        self.lname_entry.grid(row=3, column=1, sticky=tk.W)

### THIRD SCREEN
class Frame3(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "whattup"
        self.top_string = ("This is the last screen")
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=600)
        self.top_string_label = ttk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=600)
        nj_check = tk.Checkbutton(self, text='NJ')
        nj_check.grid(row=3, column=0, sticky=tk.W)
        tk.Checkbutton(self, text='NY').grid(row=4, column=0, sticky=tk.W)
        tk.Checkbutton(self, text='CT').grid(row=5, column=0, sticky=tk.W)

        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)


        
frames = [Frame1, Frame2, Frame3]
limit = len(frames)
        
### ROOT SCREEN
class Wizard(tk.Tk):
    """ JumpVisual Wizard root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("JumpVisual Photographer Coverage Wizard")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.leftframe = tk.Frame(width=300, bg="blue")
        self.i = 0
        

        #version
        tk.Label(self.leftframe, text=version, bg="blue", fg="white").grid(row=1, column=0, sticky=tk.S, padx=3, pady=3)

        #styling
   
        self.leftframe.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), rowspan=4)
        self.grid_propagate(True) 
        self.leftframe.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        
    def drawframe(self,i):
        print("i is " + str(self.i))
        self.next_button = ttk.Button(self, text="Next >>", command=lambda: Wizard.next_frame(self, self.current_frame, self.i))
        self.back_button = ttk.Button(self, text="<< Back", command=lambda: Wizard.prev_frame(self,self.current_frame, self.i))
        
        self.current_frame = frames[i](self, padx=30, pady=30, width=400)
        self.current_frame.grid(row=0,column=1)
        self.next_button.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)
        self.back_button.grid(row=3, column=2, sticky=tk.W, padx=10, pady=10)
        if self.i == (limit-1):
            self.next_button.destroy()
        if self.i == 0:
            self.back_button.destroy()


    def next_frame(self, current_frame, i):
        """advances to next frame."""
        current_frame.destroy()
        print("Next hit. Frame destroyed")
        if self.i < (len(frames)-1):
            self.i += 1
        self.drawframe(self.i)
    
    def prev_frame(self, current_frame, i):
        """returns to previous frame"""
        current_frame.destroy()
        print("Back hit. Frame destroyed")
        if self.i > 0:
            self.i -= 1
        self.drawframe(self.i)


### USER CLASS
class User(Wizard):
    """A class to hold the User's data"""
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        print("A user has been created")
        self.firstname = ''
        self.lastname = ''
        self.email = ''
        self.phone = ''
        self.address = ''
        self.slack = ''
        self.abilities = 'P'
        self.nj_bool = False
        self.ny_bool = False
        self.ct_bool = False
        self.nj_counties = []
        self.ny_counties = []
        self.ct_counties = []





        


if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    
    app = Wizard()
    user1 = User()
    app.drawframe(app.i)
    app.mainloop()
    exit()









##nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
##	'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')
##
##conn = sqlite3.connect('jump.db')
##c = conn.cursor()


##def center_window(width=300, height=200):
##    # get screen width and height
##    screen_width = root.winfo_screenwidth()
##    screen_height = root.winfo_screenheight()
##
##    # calculate position x and y coordinates
##    x = (screen_width/2) - (width/2)
##    y = (screen_height/2) - (height/2)
##    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


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

##states = input("Please enter the states that you cover, separated by spaces\n\t(e.g. nj ny ct)\n\n")
##states = states.upper()
##states = states.split()
##
##for state in states:
##	print("\n\nThe counties in " + state + " are...\n")
##	c.execute("SELECT county_name FROM UScities WHERE state_id=?", (state,))
##	holder = [tup[0] for tup in c.fetchall()]
##	counties = []
##	for county in holder:
##		if county not in counties:
##			counties.append(county)		
##	counties.sort()
##	for county in counties:
##		print(county)
##	print("===========================")
##	counties_covered = input("Please enter every county that you cover partially or completely (separated by spaces)\n")
##	counties_covered = counties_covered.upper()
##	counties_covered = counties_covered.split()
##	print("The counties you cover at least partially are...\n")
##	for county in counties_covered:
##		print(county + "   ")
##	yesno = input("\nIs this correct?")
##
##
##
##conn.close()

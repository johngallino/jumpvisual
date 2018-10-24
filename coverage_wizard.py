##import sqlite3
import tkinter as tk
from tkinter import ttk

version = "v1.0"

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
	'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')


### FIRST SCREEN
class Frame1(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
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
        
        self.next_button = ttk.Button(self, text="Next >>", command=lambda:app.next_frame(app.current_frame, app.i))
        self.next_button.grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

### SECOND SCREEN
class Frame2(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 1"
        self.top_string = ("Enter your name and contact information")
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=600)
        self.top_string_label = ttk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=600)
        info = tk.Frame(self)
        info.grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
        tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="Phone Number").grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="Email").grid(row=2, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="City of Residence").grid(row=4, column=0, sticky=tk.W)
        tk.Label(info, text="State").grid(row=4, column=1, sticky=tk.W, padx=20)
        
        self.f = tk.StringVar()
        self.l = tk.StringVar()
        self.f.set(user.firstname)
        self.l.set(user.lastname)
        self.fname_entry = tk.Entry(info, textvariable=self.f)
        self.lname_entry = tk.Entry(info, textvariable=self.l)
        self.fname_entry.grid(row=1, column=0, sticky=tk.W)
        self.lname_entry.grid(row=1, column=1, sticky=tk.W, padx=20)
        
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.phone.set(user.phone)
        self.email.set(user.email)
        self.phone_entry = tk.Entry(info, textvariable=self.phone)
        self.email_entry = tk.Entry(info, textvariable=self.email)
        self.phone_entry.grid(row=3, column=0, sticky=tk.W)
        self.email_entry.grid(row=3, column=1, sticky=tk.W, padx=20)
        
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.city.set(user.hometown)
        self.city_entry = tk.Entry(info, textvariable=self.city)
        self.choices=[ 'NJ', 'NY', 'CT' ]
        self.statevar = tk.StringVar()
        self.statepulldown = ttk.OptionMenu(info, self.statevar, self.choices[1], *self.choices)
        self.city_entry.grid(row=5, column=0, sticky=tk.W)
        self.statepulldown.grid(row=5, column=1, sticky=tk.W, padx=20)
        self.statevar.set('NJ')
        
                  
        states = tk.Frame(self, pady=20)
        states.grid(row=4, column=0, sticky=tk.W)
        tk.Label(states, text="What states does your coverage zone include?").grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.njvar = tk.IntVar()
        self.njvar.set(user.nj_bool)
        self.njbox = tk.Checkbutton(states, text='NJ', variable=self.njvar)
        self.njbox.grid(row=1, column=0, sticky=tk.W)
        self.nyvar = tk.IntVar()
        self.nyvar.set(user.ny_bool)
        self.nybox = tk.Checkbutton(states, text='NY', variable=self.nyvar)
        self.nybox.grid(row=1, column=1, sticky=tk.W, padx=20)
        self.ctvar = tk.IntVar()
        self.ctvar.set(user.ct_bool)
        self.ctbox = tk.Checkbutton(states, text='CT', variable=self.ctvar)
        self.ctbox.grid(row=1, column=2, sticky=tk.W, padx=20)
        
        services = tk.Frame(self,pady=10)
        services.grid(row=5, column=0, sticky=tk.W)
        tk.Label(services, text="Additional Services You Offer").grid(row=0, column=0, sticky=tk.W)
        self.vidvar = tk.IntVar()
        if "_V" in user.abilities:
            self.vidvar.set(1)
        tk.Checkbutton(services, text='Int/Ext Video', variable=self.vidvar).grid(row=1, column=0,sticky=tk.W)
        self.floorvar = tk.IntVar()
        if "_Fl" in user.abilities:
            self.floorvar.set(1)
        tk.Checkbutton(services, text='Floorplans', variable=self.floorvar).grid(row=2, column=0,sticky=tk.W)
        self.aesvar = tk.IntVar()
        if "_AeS" in user.abilities:
            self.aesvar.set(1)
        tk.Checkbutton(services, text='Aerial stills', variable=self.aesvar).grid(row=1, column=1,sticky=tk.W)
        self.aevvar = tk.IntVar()
        if "_AeV" in user.abilities:
            self.aevvar.set(1)
        tk.Checkbutton(services, text='Aerial video', variable=self.aevvar).grid(row=2, column=1,sticky=tk.W)
        self.faavar = tk.IntVar()
        if "_FAA" in user.abilities:
            self.faavar.set(1)
        tk.Checkbutton(services, text='FAA Certified', variable=self.faavar).grid(row=3, column=1,sticky=tk.W)
        #tk.Label(services, text=user.abilities).grid(row=4, column=0, sticky=tk.W)

        nav = tk.Frame(self)
        nav.grid(row=6, column=0, sticky=tk.E + tk.S)
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)
        
        #placing the widgets inside Frame2
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, ipady=20)
        
        
    def nxt(self, user):
        user.firstname = self.fname_entry.get()
        user.lastname = self.lname_entry.get()
        user.nj_bool = self.njvar.get()
        user.ny_bool = self.nyvar.get()
        user.ct_bool = self.ctvar.get()
        user.phone = self.phone.get()
        user.email = self.email.get()
        user.hometown = self.city.get()
        user.homestate = self.statevar.get()
        user.abilities = "P"
        if self.vidvar.get() == 1:
            user.abilities += "_V"
            print("Video added to abilities")
        if self.floorvar.get() == 1:
            user.abilities += "_Fl"
            print("Floorplans added to abilities")
        if self.aesvar.get() == 1:
            user.abilities += "_AeS"
            print("Aerial Stills added to abilities")
        if self.aevvar.get() == 1:
            user.abilities += "_AeV"
            print("Aerial Video added to abilities")
        if self.faavar.get() == 1:
            user.abilities += "_FAA"
            print("FAA Certification added to abilities")
        app.next_frame(app.current_frame, app.i)

### THIRD SCREEN
class Frame3(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print("User abilities are saved as " + user.abilities)
        self.header_string = "Step 2 - NJ Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nREMEMBER: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = ttk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        tk.Label(transfer, text="NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=2, sticky=tk.W)
        njlistbox = tk.Listbox(transfer, height=21)
        for county in nj_counties:
            njlistbox.insert(tk.END, county.title())
        njlistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        tk.Button(transfer, text="  Add >>  ").grid(row=1, column=1, padx=20)
        tk.Button(transfer, text="<< Remove").grid(row=2, column=1,padx=20)
        userlistbox = tk.Listbox(transfer, height=21)
        userlistbox.grid(row=1, column=2, rowspan=2, sticky=tk.W)
        
        #back button
        self.back_button = ttk.Button(self, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=6, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)
        
### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        print("A user has been created")
        self.firstname = ''
        self.lastname = ''
        self.email = ''
        self.phone = ''
        self.hometown = ''
        self.homestate = ''
        self.slack = ''
        self.abilities = 'P'
        self.nj_bool = False
        self.ny_bool = False
        self.ct_bool = False
        self.nj_counties = []
        self.ny_counties = []
        self.ct_counties = []

user = User()
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
        self.current_frame = frames[self.i](self, user, padx=30, pady=30, width=400)        
        
        #version
        tk.Label(self.leftframe, text=version, bg="blue", fg="white").grid(row=1, column=0, sticky=tk.S, padx=3, pady=3)

        #styling
   
        self.leftframe.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), rowspan=4)
        self.grid_propagate(True) 
        self.leftframe.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        
    def drawframe(self, i, user):
        """draws current frame"""
        print("i is " + str(i) + " limit is " + str(limit))
        
        self.current_frame = frames[i](self, user, padx=30, pady=30, width=400)        
        self.current_frame.grid(row=0,column=1)


    def next_frame(self, current_frame, i):
        """advances to next frame."""
        self.current_frame.destroy()
        self.i += 1
        self.drawframe(self.i, user)
    
    def prev_frame(self, current_frame, i):
        """returns to previous frame"""
        self.current_frame.destroy()
        self.i -= 1
        self.drawframe(self.i, user)


if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    
    app = Wizard()
    app.drawframe(app.i, user)
    app.mainloop()
    exit()





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

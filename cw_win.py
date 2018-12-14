import sqlite3
import os
import tkinter as tk
from tkinter import ttk

version = "v1.1w"
PATH = os.path.join(os.path.expanduser('~'), 'Desktop')


nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
    'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')

ny_counties = ('albany', 'allegany', 'bronx', 'broome', 'cattaraugus', 'cayuga', 'chautauqua', 'chemung', 'chenango', 'clinton', 'columbia', 'cortland', 'delaware',
               'dutchess', 'erie', 'essex', 'franklin', 'fulton', 'genesee', 'greene', 'hamilton', 'herkimer', 'jefferson', 'kings', 'lewis', 'livingston', 'madison',
               'monroe', 'montgomery', 'nassau', 'new york', 'niagra', 'oneida', 'onondaga', 'ontario', 'orange', 'orleans', 'oswego', 'otsego', 'putnam', 'queens',
               'rensselaer', 'richmond', 'rockland', 'st. lawrence', 'saratoga', 'schenectady', 'schoharie', 'schuyler', 'seneca', 'steuben', 'suffolk', 'sullivan',
               'tioga', 'tompkins', 'ulster', 'warren', 'washington', 'wayne', 'westchester', 'wyoming', 'yates')

ct_counties = ('fairfield', 'hartford', 'litchfield', 'middlesex', 'new haven', 'new london', 'tolland', 'windham')

conn = sqlite3.connect('jump.db')
c = conn.cursor()


### FIRST SCREEN
class Frame1(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "Welcome to the JumpVisual Coverage Wizard!"

        self.top_string = ("This simple program is intended for JumpVisual staff photographers. It will help you "
                        "choose the towns that you want to work in, and "
                        "generate a report at the end to input into our database. Any time you want to change your coverage areas, just use this tool to generate a new file."
                        "\n\nLet's get started!")

        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 20), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont"), wraplength=500)
        
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
        self.top_string = ("Let's first fill out your profile. Enter your name, contact information, and the services you provide.")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 20), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont"), wraplength=500)
        info = tk.Frame(self)
        info.grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
        tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="Phone Number").grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="Email").grid(row=2, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="City of Residence").grid(row=4, column=0, sticky=tk.W)
        tk.Label(info, text="State").grid(row=4, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="Slack Handle").grid(row=7, column=0, sticky=tk.W)
        
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
        
        self.slack = tk.StringVar()
        self.slack.set(user.slack)
        self.slack_entry = tk.Entry(info, textvariable=self.slack)
        self.slack_entry.grid(row=8, column=0, sticky=tk.W)
                  
        states = tk.Frame(self, pady=10)
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
        #self.ctbox.grid(row=1, column=2, sticky=tk.W, padx=20)
        
        services = tk.Frame(self,pady=10)
        services.grid(row=7, column=0, sticky=tk.W)
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
        nav.grid(row=8, column=0, sticky=tk.E + tk.S)
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
        user.slack = self.slack.get()
        user.hometown = self.city.get()
        user.homestate = self.statevar.get()
        user.abilities = "P"
        if self.vidvar.get() == 1:
            user.abilities += "_V"
            ##print("Video added to abilities")
        if self.floorvar.get() == 1:
            user.abilities += "_Fl"
            ##print("Floorplans added to abilities")
        if self.aesvar.get() == 1:
            user.abilities += "_AeS"
            ##print("Aerial Stills added to abilities")
        if self.aevvar.get() == 1:
            user.abilities += "_AeV"
            ##print("Aerial Video added to abilities")
        if self.faavar.get() == 1:
            user.abilities += "_FAA"
            ##print("FAA Certification added to abilities")
        if user.firstname == "" or user.lastname == "" or user.phone == "" or user.email == "" or user.hometown == "":
            tk.Label(self, text="You must fill out all info above to proceed!", fg="red").grid(row=3, column=0, sticky=tk.W)
        elif not user.nj_bool and not user.ny_bool and not user.ct_bool:
            tk.Label(self, text="You must check at lease one state!", fg="red").grid(row=6, column=0, sticky=tk.W)
        else:
           #print (user.firstname)
            app.choose_frames(user)
            app.next_frame(app.current_frame, app.i)

### THIRD SCREEN
class NJCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        user.nj_counties.clear()
        self.header_string = "Step 2 - New Jersey Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 20), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont"), wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.njlistbox = tk.Listbox(transfer, height=15)
        self.njlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.njlistbox['yscrollcommand'] = self.njlistbox_scroll.set
        self.njlistbox_scroll['command'] = self.njlistbox.yview
        for county in nj_counties:
            self.njlistbox.insert(tk.END, county.title())
            
        self.njlistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.njlistbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=15)
        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

    def add_county(self, user):
        #items = map(int,self.njlistbox.curselection())
        #for item in items:
        self.userlistbox.insert(tk.END, self.njlistbox.get(tk.ACTIVE))
        user.nj_counties.append(self.njlistbox.get(tk.ACTIVE))
        self.njlistbox.delete(tk.ACTIVE)
            
    def del_county(self, user):
        self.njlistbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        user.nj_counties.remove(self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
    def nxt(self, user):
        ##print(user.nj_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            app.next_frame(app.current_frame, app.i)
        
###FOURTH SCREEN
class NJTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 3 - NJ Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to your coverage zone.\n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 20), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont"), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset NJ towns if there are any
        if len(user.nj_towns) !=0:
            user.nj_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NJ COUNTIES
        tk.Label(transfer, text="Your NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        self.njlistbox = tk.Listbox(transfer, height=4, width=20)
        self.njlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.njlistbox['yscrollcommand'] = self.njlistbox_scroll.set
        self.njlistbox_scroll['command'] = self.njlistbox.yview
        self.njlistbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.njlistbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        
        
        for county in user.nj_counties:
            self.njlistbox.insert(tk.END, county.title())
            
        #### TOWN BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=10, width=20)
        self.townbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.townbox['yscrollcommand'] = self.townbox_scroll.set
        self.townbox_scroll['command'] = self.townbox.yview
        self.townbox.grid(row=3, column=0, rowspan=2, sticky=tk.W)
        self.townbox_scroll.grid(row=3, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E)
        
        county = self.njlistbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=?", (county,))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        
        for town in holder:
            self.townbox.insert(tk.END, town.title())
            
        
      
        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        
        ### USER BOX
        tk.Label(transfer, text="Your NJ Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=15, width=20)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.nj_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
            
    def del_town(self, user):
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        user.nj_towns.remove(self.townbox.get(tk.ACTIVE))
        
        
    def view_towns(self):
        self.townbox.delete(0, tk.END) # clear
        county = self.njlistbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=?", (county,))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user):
        ##print(user.nj_counties)
        ##print(user.nj_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            app.next_frame(app.current_frame, app.i)
        
### NY COUNTIES
class NYCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        user.ny_counties.clear()
        self.header_string = "Step 2 - New York Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 20), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont"), justify="left", wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NY Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.nylistbox = tk.Listbox(transfer, height=15)
        self.nylistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.nylistbox['yscrollcommand'] = self.nylistbox_scroll.set
        self.nylistbox_scroll['command'] = self.nylistbox.yview
        for county in ny_counties:
            self.nylistbox.insert(tk.END, county.title())
            
        self.nylistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.nylistbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=15)
        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

    def add_county(self, user):
        #items = map(int,self.nylistbox.curselection())
        #for item in items:
        self.userlistbox.insert(tk.END, self.nylistbox.get(tk.ACTIVE))
        user.ny_counties.append(self.nylistbox.get(tk.ACTIVE))
        self.nylistbox.delete(tk.ACTIVE)
            
    def del_county(self, user):
        self.nylistbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        user.ny_counties.remove(self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
    def nxt(self, user):
        ##print(user.ny_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            app.next_frame(app.current_frame, app.i)
        
### NY TOWNS
class NYTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 3 - NY Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to your coverage zone. \n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 20),justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont"), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset NY towns if there are any
        if len(user.ny_towns) !=0:
            user.ny_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NJ COUNTIES
        tk.Label(transfer, text="Your NY Counties:").grid(row=0, column=0, sticky=tk.W)
        self.nylistbox = tk.Listbox(transfer, height=4, width=20)
        self.nylistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.nylistbox['yscrollcommand'] = self.nylistbox_scroll.set
        self.nylistbox_scroll['command'] = self.nylistbox.yview
        self.nylistbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.nylistbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        
        
        for county in user.ny_counties:
            self.nylistbox.insert(tk.END, county.title())
            
        #### TOWN BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=10, width=20)
        self.townbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.townbox['yscrollcommand'] = self.townbox_scroll.set
        self.townbox_scroll['command'] = self.townbox.yview
        self.townbox.grid(row=3, column=0, rowspan=2, sticky=tk.W)
        self.townbox_scroll.grid(row=3, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E)
        
        county = self.nylistbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=?", (county,))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        
        for town in holder:
            self.townbox.insert(tk.END, town.title())
            
        
      
        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        
        ### USER BOX
        tk.Label(transfer, text="Your NY Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=15, width=20)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.ny_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
            
    def del_town(self, user):
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        user.ny_towns.remove(self.townbox.get(tk.ACTIVE))
        
        
    def view_towns(self):
        self.townbox.delete(0, tk.END) # clear
        county = self.nylistbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=?", (county,))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user):
        ##print(user.ny_counties)
        ##print(user.ny_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            app.next_frame(app.current_frame, app.i)
        
class FinalFrame(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "Finishing Up!"

        self.top_string = "You're done! Check out the information below and make sure it's correct. When you hit the Export button, a new file titled '" + user.firstname.title() +user.lastname.title() + ".jmp' will be created on your Desktop.\n\nIMPORTANT: Send the generated .jmp file to @gallino on Slack"

        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 20), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont"), wraplength=500)
        # Proof
        report = tk.Frame(self)
        report.grid(row=3, column=0, sticky=tk.W+tk.E)
        self.proof = tk.Text(report, height=18, width=60)
        self.proof_scroll = tk.Scrollbar(report, orient=tk.VERTICAL)
        self.proof['yscrollcommand'] = self.proof_scroll.set
        self.proof_scroll['command'] = self.proof.yview
        self.proof_scroll.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)
        self.proof.insert(tk.END, "Name:\t" + user.firstname.title() + " " + user.lastname.title() + "\n")
        self.proof.insert(tk.END, "Phone:\t" + user.phone + "\n")
        self.proof.insert(tk.END, "Email:\t" + user.email + "\n")
        self.proof.insert(tk.END, "City:\t" + user.hometown + ", " + user.homestate+ "\n")
        self.proof.insert(tk.END, "Services:\t" + user.abilities + "\n\n")
        self.proof.insert(tk.END, "### COVERAGE ZONE ###\n")
        self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns
        
        for town in self.usertowns:
            self.proof.insert(tk.END, town + "\n")
        self.proof.config(state=tk.DISABLED)
        self.proof.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        nav = tk.Frame(self)
        nav.grid(row=5, column=0, sticky=tk.E)
        
        self.finlabel = tk.Label(report, text="File generated! You may now exit the program :)", anchor=tk.W)
        self.export_button = ttk.Button(report, text="Export", command=lambda:self.next(user))
        self.export_button.grid(row=2, column=1, sticky=tk.E, pady=10)
        
        
        #exit button
        #self.exit_button = ttk.Button(nav, text="Exit", command=app.quit())
        #self.exit_button.grid(row=0, column=1, sticky=tk.E)

        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:app.prev_frame(app.current_frame, app.i))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, columnspan=2, ipady=20)
        
    def next(self, user):
        self.finlabel.grid(row=2, column=0, sticky=tk.W)
        app.generate(user)
    


        

        
### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        ##print("A user has been created")
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
        self.nj_towns = []
        self.ny_towns = []
        self.ct_towns = []

user = User()


        
### ROOT SCREEN
class Wizard(tk.Tk):
    """ JumpVisual Wizard root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.frames = [Frame1, Frame2]
        self.limit = len(self.frames)
        self.wm_iconbitmap('jump-wizard-round.ico')
        self.title("JumpVisual Photographer Coverage Wizard")
        self.geometry("850x600")
        self.resizable(width=False, height=False)
        self.leftframe = tk.Frame(width=200)
        self.i = 0
        self.current_frame = self.frames[self.i](self, user, padx=30, pady=30, width=400)
        self.img = tk.PhotoImage(file="jump.pbm") 
        
        #version
        tk.Label(self.leftframe, image=self.img).grid(row=0, column=0, sticky=tk.N + tk.S)
        tk.Label(self.leftframe, text=version, justify=tk.LEFT).place(x=1, y=1, anchor=tk.NW)

        #styling
   
        self.leftframe.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), rowspan=4)
        self.grid_propagate(True) 
        self.leftframe.rowconfigure(0, weight=1)
        self.leftframe.columnconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def choose_frames(self, user):
        ##print(self.frames)
        self.frames = [Frame1, Frame2]
        if user.nj_bool:
            self.frames.append(NJCounties)
        if user.ny_bool:
            self.frames.append(NYCounties)
        if user.ct_bool:
            self.frames.append(CTCounties)
        if user.nj_bool:
            self.frames.append(NJTowns)
        if user.ny_bool:
            self.frames.append(NYTowns)
        if user.ct_bool:
            self.frames.append(CTTowns)
        self.frames.append(FinalFrame)   
        self.limit = len(self.frames)
        ##print(self.frames)
        
        
    def drawframe(self, i, user):
        """draws current frame"""
        #print("i is " + str(i) + " limit is " + str(self.limit))
        
        self.current_frame = self.frames[i](self, user, padx=30, pady=30, width=400)        
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
    
    def generate(self, user):
        filename = user.firstname.title() + user.lastname.title() + '.jmp'
        try:
            file = open(os.path.join(PATH, filename), "w")
            file.write("#\tTo edit your contact info or coverage, you can run the wizard\n#\tagain or make changes to this file directly using Notepad (win)\n#\tor Textedit (mac). ")
            file.write("DO NOT add towns to this list that did not\n#\tappear in the wizard. Please notify johngallino@gmail.com or\n#\t@gallino on Slack about any missing towns.\n")
            file.write(user.firstname + " " + user.lastname + "\n")
            file.write(user.phone + "\n")
            file.write(user.email + "\n")
            file.write(user.hometown + " " + user.homestate + "\n")
            file.write(user.slack + "\n")
            file.write(user.abilities + "\n")
            self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns
            for town in self.usertowns:
                if town is not None:
                    file.write(town.rstrip('\n') + "\n")
            
            file.close()
        except:
            error = tk.Toplevel(self, text="Uh oh. I had trouble writing the file!" )
            error.title("Bad news")
            tk.Button(error, text="oh well", command=self.destroy())


if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    
    app = Wizard()
    app.drawframe(app.i, user)
    app.mainloop()
    raise SystemExit



##def center_window(width=200, height=200):
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
#   yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
#   states_covered.append('NJ')

# yesno = input("Do you cover any parts of NEW YORK? (y/n)")
# while lower(yesno) != 'y' && lower(yesno) != 'n':
#   yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
#   states_covered.append('NY')

# yesno = input("Do you cover any parts of CONNECTICUT? (y/n)")
# while lower(yesno) != 'y' && lower(yesno) != 'n':
#   yesno = input("Please input Y or N")
# if lower(yesno) = 'y':
#   states_covered.append('CT')

##states = input("Please enter the states that you cover, separated by spaces\n\t(e.g. nj ny ct)\n\n")
##states = states.upper()
##states = states.split()
##
##for state in states:
##  #print("\n\nThe counties in " + state + " are...\n")
##  c.execute("SELECT county_name FROM UScities WHERE state_id=?", (state,))
##  holder = [tup[0] for tup in c.fetchall()]
##  counties = []
##  for county in holder:
##      if county not in counties:
##          counties.append(county)     
##  counties.sort()
##  for county in counties:
##      #print(county)
##  #print("===========================")
##  counties_covered = input("Please enter every county that you cover partially or completely (separated by spaces)\n")
##  counties_covered = counties_covered.upper()
##  counties_covered = counties_covered.split()
##  #print("The counties you cover at least partially are...\n")
##  for county in counties_covered:
##      #print(county + "   ")
##  yesno = input("\nIs this correct?")
##
##
##
##conn.close()

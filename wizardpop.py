import sqlite3
import os
import tkinter as tk
from tkinter import ttk

version = "v2.0"

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
    'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'somerset', 'sussex', 'union', 'warren')

ny_counties = ('albany', 'allegany', 'bronx', 'broome', 'cattaraugus', 'cayuga', 'chautauqua', 'chemung', 'chenango', 'clinton', 'columbia', 'cortland', 'delaware',
               'dutchess', 'erie', 'essex', 'franklin', 'fulton', 'genesee', 'greene', 'hamilton', 'herkimer', 'jefferson', 'kings', 'lewis', 'livingston', 'madison',
               'monroe', 'montgomery', 'nassau', 'new york', 'niagra', 'oneida', 'onondaga', 'ontario', 'orange', 'orleans', 'oswego', 'otsego', 'putnam', 'queens',
               'rensselaer', 'richmond', 'rockland', 'st. lawrence', 'saratoga', 'schenectady', 'schoharie', 'schuyler', 'seneca', 'steuben', 'suffolk', 'sullivan',
               'tioga', 'tompkins', 'ulster', 'warren', 'washington', 'wayne', 'westchester', 'wyoming', 'yates')

ct_counties = ('fairfield', 'hartford', 'litchfield', 'middlesex', 'new haven', 'new london', 'tolland', 'windham')

found = os.path.isfile('jump.db')
c = 0 #global variable
i = 0

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = win.winfo_screenwidth() // 2 -200
    y = win.winfo_screenheight() // 2 - 200
    width = 360
    height = 180
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def checkjumpdb():
    """see if jump.db file is present"""
    if not found:
        dberror = tk.Toplevel(padx=15, pady=15)
        tk.Label(dberror, text="Missing jump.db file").grid(padx=20, pady=20, sticky='ew')
        def shutdown():
                raise SystemExit
        tk.Button(dberror, text="OK", command=shutdown).grid(row=1, column=0, sticky='ew', ipadx=15)
    else:
        global conn
        conn = sqlite3.connect('jump.db')
        global c 
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
                                 font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        if not found:
            tk.Label(self, text="Uh oh! Can't find the jump.db file. Please place it in the same folder as the .exe file and start the program again.", fg="RED", wraplength=300).grid(row=3, column=0, sticky='ew')
        else:
            self.next_button = ttk.Button(self, text="Next >>", command=lambda:next_frame(current_frame))
            self.next_button.grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)

### SECOND SCREEN
class Frame2(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.header_string = "Step 1"

        if not found:
            tk.Label(self, text="Uh oh! Can't find the jump.db file. Please place it in the same folder as the .exe file and start the program again.", fg="RED", wraplength=300).grid(row=3, column=0, sticky='ew')
            
        self.top_string = ("Let's first fill out your profile. Enter your name, contact information, and the services you provide.")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, ipady=8)

        info = tk.Frame(self)
        info.grid(row=2, column=0, rowspan=3, sticky=tk.W)
        tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
        tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W)
        tk.Label(info, text="Phone Number").grid(row=2, column=1, sticky=tk.W)
        tk.Label(info, text="Address").grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="City of Residence").grid(row=4, column=0, sticky=tk.W)
        tk.Label(info, text="State").grid(row=4, column=1, sticky=tk.W,)
        tk.Label(info, text="Email").grid(row=6, column=0, sticky=tk.W,)
        tk.Label(info, text="JumpVisual Email").grid(row=6, column=1, sticky=tk.W)
        tk.Label(info, text="Birthday (MM/DD)").grid(row=8, column=0, sticky=tk.W)
        tk.Label(info, text="FAA Certification #").grid(row=8, column=1, sticky=tk.W)
        tk.Label(info, text="Zip").grid(row=4,column=1, sticky=tk.E)
        emergency = tk.Frame(info, bd=1, relief=tk.GROOVE)
        emergency.grid(row=11, column = 0, sticky='nsw', pady=(10,0), ipady=5, columnspan=3)
        tk.Label(emergency, text="Emergency Contact").grid(row=0, column=0, sticky='w', padx=5, pady=(0,10))
        tk.Label(emergency, text="Name").grid(row=1, column=0, sticky='w', padx=5,)
        tk.Label(emergency, text="Relation").grid(row=1, column=1, sticky='w', padx=5,)
        tk.Label(emergency, text="Phone Number").grid(row=3, column=0, sticky='w', padx=5,)
        
        self.f = tk.StringVar()
        self.f.set(user.firstname)
        self.fname_entry = tk.Entry(info, textvariable=self.f)
        self.fname_entry.grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        
        self.l = tk.StringVar()
        self.l.set(user.lastname)
        self.lname_entry = tk.Entry(info, textvariable=self.l)
        self.lname_entry.grid(row=1, column=1, sticky=tk.W,)
        
        self.address = tk.StringVar()
        self.address.set(user.address)
        self.address_entry = tk.Entry(info, textvariable=self.address)
        self.address_entry.grid(row=3, column=0, sticky=tk.W)
        
        self.phone = tk.StringVar()
        self.phone.set(user.phone)
        self.phone_entry = tk.Entry(info, textvariable=self.phone)
        self.phone_entry.grid(row=3, column=1, sticky=tk.W)
        
        self.city = tk.StringVar()
        self.city.set(user.hometown)
        self.city_entry = tk.Entry(info, textvariable=self.city)
        self.city_entry.grid(row=5, column=0, sticky=tk.W)
        
        self.state = tk.StringVar()
        self.choices=[ 'NJ', 'NY', 'CT', 'PA' ]
        self.statevar = tk.StringVar()
        self.statepulldown = ttk.OptionMenu(info, self.statevar, self.choices[1], *self.choices)
        self.statepulldown.grid(row=5, column=1, sticky=tk.W)
        self.statevar.set(user.homestate)
        
        self.zip = tk.StringVar()
        self.zip.set(user.zip)
        self.zip_entry = tk.Entry(info, width=8, textvariable=self.zip)
        self.zip_entry.grid(row=5, column=1, sticky=tk.E)
        
        self.email = tk.StringVar()
        self.email.set(user.email)
        self.email_entry = tk.Entry(info, textvariable=self.email)
        self.email_entry.grid(row=7, column=0, sticky=tk.W)
        
        self.jvemail = tk.StringVar()
        self.jvemail.set(user.jvemail)
        self.jvemail_entry = tk.Entry(info, textvariable=self.jvemail)
        self.jvemail_entry.grid(row=7, column=1, sticky=tk.W)
        
        self.birthday = tk.StringVar()
        self.birthday.set(user.birthday)
        self.birthday_entry = tk.Entry(info, textvariable=self.birthday)
        self.birthday_entry.grid(row=9, column=0, sticky=tk.W)
        
        self.faa_num = tk.StringVar()
        self.faa_num.set(user.faa_num)
        self.faa_num_entry = tk.Entry(info, textvariable=self.faa_num)
        self.faa_num_entry.grid(row=9, column=1, sticky=tk.W)
        
        self.emer_name = tk.StringVar()
        self.emer_name.set(user.emer_name)
        self.emer_name_entry = tk.Entry(emergency, textvariable=self.emer_name)
        self.emer_name_entry.grid(row=2, column=0, sticky=tk.W, padx=(5, 20))
        
        self.emer_relation = tk.StringVar()
        self.emer_relation.set(user.emer_relation)
        self.emer_relation_entry = tk.Entry(emergency, width=17, textvariable=self.emer_relation)
        self.emer_relation_entry.grid(row=2, column=1, sticky=tk.W, padx=5,)
        
        self.emer_cell = tk.StringVar()
        self.emer_cell.set(user.emer_name)
        self.emer_cell_entry = tk.Entry(emergency, textvariable=self.emer_cell)
        self.emer_cell_entry.grid(row=4, column=0, sticky=tk.W, padx=5,)
                  
        states = tk.Frame(info, pady=5)
        states.grid(row=10, column=0, columnspan=3, sticky=tk.W)
        tk.Label(states, text="What areas does your coverage zone include?").grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.njvar = tk.IntVar()
        self.njvar.set(user.nj_bool)
        self.njbox = tk.Checkbutton(states, text='NJ', variable=self.njvar)
        self.njbox.grid(row=1, column=0, sticky=tk.W)
        self.nyvar = tk.IntVar()
        self.nyvar.set(user.ny_bool)
        self.nybox = tk.Checkbutton(states, text='NY', variable=self.nyvar)
        self.nybox.grid(row=1, column=1, sticky=tk.W, padx=10)
#        self.manvar = tk.IntVar()
#        self.manvar.set(user.man_bool)
#        self.manbox = tk.Checkbutton(states, text='Manhattan', variable=self.manvar)
#        self.manbox.grid(row=1, column=2, sticky=tk.W, padx=10)
        self.ctvar = tk.IntVar()
        self.ctvar.set(user.ct_bool)
        self.ctbox = tk.Checkbutton(states, text='CT', variable=self.ctvar)
        self.ctbox.grid(row=1, column=2, sticky=tk.W, padx=10)
        
        tk.Label(info, text="Check all that apply").grid(row=0, column=2, sticky='nw', padx=(15,0))
        services = tk.LabelFrame(info, pady=2)
        services.grid(row=1, column=2, rowspan=25, sticky='nw', padx=(15,0))
        self.weekendsvar = tk.IntVar()
        if "WkEnds/" in user.abilities:
            self.weekendsvar.set(1)
        tk.Checkbutton(services, text='Work Weekends', variable=self.weekendsvar).grid(row=1, column=0, sticky=tk.W)
        self.floorvar = tk.IntVar()
        if "FP/" in user.abilities:
            self.floorvar.set(1)
        tk.Checkbutton(services, text='Floorplans', variable=self.floorvar).grid(row=2, column=0,sticky=tk.W)
        self.duvar = tk.IntVar()
        if "Pdusk/" in user.abilities:
            self.duvar.set(1)
        tk.Checkbutton(services, text='Dusk Photography', variable=self.duvar).grid(row=3, column=0, padx=(0,5), sticky=tk.W)
        self.aesvar = tk.IntVar()
        if "Paerial/" in user.abilities:
            self.aesvar.set(1)
        tk.Checkbutton(services, text='Aerial stills', variable=self.aesvar).grid(row=4, column=0,sticky=tk.W)
        self.faavar = tk.IntVar()
        if "FAA/" in user.abilities:
            self.faavar.set(1)
        tk.Checkbutton(services, text='FAA Certified', variable=self.faavar).grid(row=5, column=0,sticky=tk.W)
        self.a_insvar = tk.IntVar()
        if "InsAerial/" in user.abilities:
            self.a_insvar.set(1)
        tk.Checkbutton(services, text='Aerial Insurance', variable=self.a_insvar).grid(row=6, column=0,sticky=tk.W)
        self.l_insvar = tk.IntVar()
        if "InsLiability/" in user.abilities:
            self.l_insvar.set(1)
        tk.Checkbutton(services, text='Liability Insurance', variable=self.l_insvar).grid(row=7, column=0,sticky=tk.W)
        
        tk.Label(services, text="VIDEO SERVICES").grid(row=8, column=0, sticky='ew', pady=(20, 5))
        videoframe = tk.Frame(services, borderwidth=0, relief=tk.GROOVE)
        videoframe.grid(row=9, column=0, sticky=tk.W, rowspan=7)
        self.matvar = tk.IntVar()
        if "Vmatter/" in user.abilities:
            self.matvar.set(1)
        tk.Checkbutton(videoframe, text='Matterport', variable=self.matvar).grid(row=0, column=0,sticky=tk.W)
        self.teaservar = tk.IntVar()
        if "Vteaser/" in user.abilities:
            self.teaservar.set(1)
        tk.Checkbutton(videoframe, text="Teaser Video", variable=self.teaservar).grid(row=1, column=0,  sticky=tk.W)
        self.premvar = tk.IntVar()
        if "Vpremium/" in user.abilities:
            self.premvar.set(1)
        tk.Checkbutton(videoframe, text="Premium Video", variable=self.premvar).grid(row=2, column=0,  sticky=tk.W)
        self.luxvar = tk.IntVar()
        if "Vluxury/" in user.abilities:
            self.luxvar.set(1)
        tk.Checkbutton(videoframe, text="Luxury Video", variable=self.luxvar).grid(row=3, column=0, sticky=tk.W)
        self.aevvar = tk.IntVar()
        if "Vaerial/" in user.abilities:
            self.aevvar.set(1)
        tk.Checkbutton(videoframe, text='Aerial video', variable=self.aevvar).grid(row=4, column=0, sticky=tk.W)
        self.veditvar = tk.IntVar()
        if "Vediting/" in user.abilities:
            self.veditvar.set(1)
        tk.Checkbutton(videoframe, text="Video Editing", variable=self.veditvar).grid(row=5, column=0, sticky=tk.W)
        
        
        #tk.Label(services, text=user.abilities).grid(row=4, column=0, sticky=tk.W)

        nav = tk.Frame(self)
        nav.grid(row=8, column=0, sticky=tk.E + tk.S)
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
  
        
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        

            
        if not found:
            tk.Label(self, text="Uh oh! Can't find the jump.db file. Please place it in the same folder as the .exe file and start the program again.",
                     fg="RED", wraplength=300).grid(row=9, column=0, sticky='ew')
            self.next_button.destroy()
        #back button
#        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
#        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)
    
        
        
    def nxt(self, user):
        user.firstname = self.fname_entry.get().rstrip()
        user.lastname = self.lname_entry.get().rstrip()
        user.nj_bool = self.njvar.get()
        user.ny_bool = self.nyvar.get()
#        user.man_bool = self.manvar.get()
        user.ct_bool = self.ctvar.get()
        user.phone = self.phone.get()
        user.email = self.email.get().rstrip()
        user.jvemail = self.jvemail.get().rstrip()
        user.address = self.address.get().rstrip()
        user.birthday = self.birthday.get().rstrip()
        user.faa_num = self.faa_num.get()
        user.emer_name = self.emer_name.get().rstrip()
        user.emer_relation = self.emer_relation.get().rstrip()
        user.emer_cell = self.emer_cell.get().rstrip()
        user.hometown = self.city.get().rstrip()
        user.homestate = self.statevar.get()
        user.zip = self.zip.get().rstrip()
        user.abilities = ""
        if self.weekendsvar.get() == 1:
            user.abilities += "WkEnds/"
            ##print("Video added to abilities")
        if self.floorvar.get() == 1:
            user.abilities += "FP/"
            ##print("Floorplans added to abilities")
        if self.duvar.get() == 1:
            user.abilities += "Pdusk/"
            ##print("Dusk photography added to abilities")
        if self.aesvar.get() == 1:
            user.abilities += "Paerial/"
            ##print("Aerial Stills added to abilities")
        if self.faavar.get() == 1:
            user.abilities += "FAA/"
            ##print("FAA Certification added to abilities")
        if self.matvar.get() == 1:
            user.abilities += "Vmatter/"
            ##print("Matterport added to abilities")
        if self.teaservar.get() == 1:
            user.abilities += "Vteaser/"
            ##print("Teaser video added to abilities")
        if self.premvar.get() == 1:
            user.abilities += "Vpremium/"
            ##print("Premium Video added to abilities")
        if self.luxvar.get() == 1:
            user.abilities += "Vluxury/"
            ##print("Luxury Video added to abilities")
        if self.aevvar.get() == 1:
            user.abilities += "Vaerial/"
            ##print("Aerial Video added to abilities")
        if self.veditvar.get() == 1:
            user.abilities += "Vediting/"
        if self.a_insvar.get() == 1:
            user.abilities += "InsAerial/"
        if self.l_insvar.get() == 1:
            user.abilities += "InsLiability/"

        # if user.firstname == "" or user.lastname == "" or user.phone == "" or user.email == "" or user.hometown == "":
        if user.firstname == "" or user.lastname == "":
            tk.Label(self, text="You must fill out name, phone, email, & city to proceed!", fg="red").grid(row=5, column=0, sticky=tk.W)
        elif not user.nj_bool and not user.ny_bool and not user.ct_bool:
            tk.Label(self, text="You must check at lease one state!", fg="red").grid(row=6, column=0, sticky=tk.W)
        else:
           #print (user.firstname)
            choose_frames(user)
            next_frame(current_frame)

### THIRD SCREEN
class NJCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print("User abilities are saved as " + user.abilities)
        #update sidebar
        global sidebar
        global leftframe
        global njimage
        sidebar = tk.Label(leftframe, image=njimage)
        sidebar.image = njimage
        sidebar.grid(row=0, column=0, sticky=tk.N + tk.S)
        global versionlabel
        versionlabel = tk.Label(leftframe, text=version, justify=tk.LEFT)
        versionlabel.place(x=1, y=1, anchor=tk.NW)
        
        user.nj_counties.clear()
        self.header_string = "Step 2 - New Jersey Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.njlistbox = tk.Listbox(transfer, height=21)
        self.njlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.njlistbox['yscrollcommand'] = self.njlistbox_scroll.set
        self.njlistbox_scroll['command'] = self.njlistbox.yview
        for county in nj_counties:
            self.njlistbox.insert(tk.END, county.title())
            
        self.njlistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.njlistbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=21)
        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

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
            next_frame(current_frame)
            
        
###FOURTH SCREEN
class NJTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 3 - NJ Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to your coverage zone.\n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset NJ towns if there are any
        #if len(user.nj_towns) !=0:
            #user.nj_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NJ COUNTIES
        tk.Label(transfer, text="Your NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        self.njlistbox = tk.Listbox(transfer, height=4, width=25)
        self.njlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.njlistbox['yscrollcommand'] = self.njlistbox_scroll.set
        self.njlistbox_scroll['command'] = self.njlistbox.yview
        self.njlistbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.njlistbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        
        
        for county in user.nj_counties:
            self.njlistbox.insert(tk.END, county.title())
            
        #### TOWN BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=16, width=25)
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
        self.userlistbox = tk.Listbox(transfer, height=21, width=25)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.nj_towns) != 0:
            for town in user.nj_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.nj_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
            
    def del_town(self, user):
        user.nj_towns.remove(self.userlistbox.get(tk.ACTIVE))
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
        
        
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
            next_frame(current_frame)
        
### NY COUNTIES
class NYCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        #update sidebar
        global sidebar
        global leftframe
        global nyimage
        sidebar.destroy()
        sidebar = tk.Label(leftframe, image=nyimage)
        sidebar.grid(row=0, column=0, sticky=tk.N + tk.S)
        global versionlabel
        versionlabel = tk.Label(leftframe, text=version, justify=tk.LEFT)
        versionlabel.place(x=1, y=1, anchor=tk.NW)
        
        user.ny_counties.clear()
        self.header_string = "Step 2 - New York Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NY Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.nylistbox = tk.Listbox(transfer, height=21)
        self.nylistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.nylistbox['yscrollcommand'] = self.nylistbox_scroll.set
        self.nylistbox_scroll['command'] = self.nylistbox.yview
        for county in ny_counties:
            self.nylistbox.insert(tk.END, county.title())
            
        self.nylistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.nylistbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=21)
        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

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
            next_frame(current_frame)
        
### NY TOWNS
class NYTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        img = tk.PhotoImage(file="s_ny.pbm") 
        self.header_string = "Step 3 - NY Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to your coverage zone. \n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16),justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset NY towns if there are any
#        if len(user.ny_towns) !=0:
#            user.ny_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NJ COUNTIES
        tk.Label(transfer, text="Your NY Counties:").grid(row=0, column=0, sticky=tk.W)
        self.nylistbox = tk.Listbox(transfer, height=4, width=25)
        self.nylistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.nylistbox['yscrollcommand'] = self.nylistbox_scroll.set
        self.nylistbox_scroll['command'] = self.nylistbox.yview
        self.nylistbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.nylistbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        
        
        for county in user.ny_counties:
            self.nylistbox.insert(tk.END, county.title())
            
        #### TOWN BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=16, width=25)
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
        self.userlistbox = tk.Listbox(transfer, height=21, width=25)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.ny_towns) != 0:
            for town in user.ny_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.ny_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
            
    def del_town(self, user):
        user.ny_towns.remove(self.userlistbox.get(tk.ACTIVE))
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
        
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
            next_frame(current_frame)
            
## CONNECTICUT            
class CTCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        #update sidebar
        global sidebar
        global leftframe
        global ctimage
        sidebar.destroy()
        sidebar = tk.Label(leftframe, image=ctimage)
        sidebar.grid(row=0, column=0, sticky=tk.N + tk.S)
        global versionlabel
        versionlabel = tk.Label(leftframe, text=version, justify=tk.LEFT)
        versionlabel.place(x=1, y=1, anchor=tk.NW)
        
        user.ct_counties.clear()
        self.header_string = "Step 2 - Connecticut Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of your coverage zone. Please select the counties that your coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="CT Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Your Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.CTlistbox = tk.Listbox(transfer, height=21)
        self.CTlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.CTlistbox['yscrollcommand'] = self.CTlistbox_scroll.set
        self.CTlistbox_scroll['command'] = self.CTlistbox.yview
        for county in ct_counties:
            self.CTlistbox.insert(tk.END, county.title())
            
        self.CTlistbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.CTlistbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=21)
        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_county(self, user):
        #items = map(int,self.CTlistbox.curselection())
        #for item in items:
        self.userlistbox.insert(tk.END, self.CTlistbox.get(tk.ACTIVE))
        user.ct_counties.append(self.CTlistbox.get(tk.ACTIVE))
        self.CTlistbox.delete(tk.ACTIVE)
            
    def del_county(self, user):
        self.CTlistbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        user.ct_counties.remove(self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
    def nxt(self, user):
        ##print(user.ct_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            next_frame(current_frame)
            
class CTTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        img = tk.PhotoImage(file="s_ct.pbm") 
        self.header_string = "Step 3 - CT Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to your coverage zone. \n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16),justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset ct towns if there are act
#        if len(user.ct_towns) !=0:
#            user.ct_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NJ COUNTIES
        tk.Label(transfer, text="Your CT Counties:").grid(row=0, column=0, sticky=tk.W)
        self.ctlistbox = tk.Listbox(transfer, height=4, width=25)
        self.ctlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.ctlistbox['yscrollcommand'] = self.ctlistbox_scroll.set
        self.ctlistbox_scroll['command'] = self.ctlistbox.yview
        self.ctlistbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.ctlistbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        
        
        for county in user.ct_counties:
            self.ctlistbox.insert(tk.END, county.title())
            
        #### TOWN BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=16, width=25)
        self.townbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.townbox['yscrollcommand'] = self.townbox_scroll.set
        self.townbox_scroll['command'] = self.townbox.yview
        self.townbox_hscroll = tk.Scrollbar(transfer,orient=tk.HORIZONTAL)
        self.townbox['xscrollcommand'] = self.townbox_hscroll.set
        self.townbox_hscroll['command'] = self.townbox.xview
        self.townbox_hscroll.grid(row=4, column=0, sticky='ews')
        self.townbox.grid(row=3, column=0, rowspan=2, sticky=tk.W)
        self.townbox_scroll.grid(row=3, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E)
        
        county = self.ctlistbox.get(tk.ACTIVE)
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
        tk.Label(transfer, text="Your CT Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=21, width=25)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.ct_towns) != 0:
            for town in user.ct_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.ct_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
            
    def del_town(self, user):
        user.ct_towns.remove(self.userlistbox.get(tk.ACTIVE))
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
        
    def view_towns(self):
        self.townbox.delete(0, tk.END) # clear
        county = self.ctlistbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=?", (county,))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user):
        ##print(user.ct_counties)
        ##print(user.ct_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to your coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            next_frame(current_frame)
        
class FinalFrame(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #update sidebar
        global sidebar
        global leftframe
        global baseimage
        sidebar.destroy()
        sidebar = tk.Label(leftframe, image=baseimage)
        sidebar.grid(row=0, column=0, sticky=tk.N + tk.S)
        global versionlabel
        versionlabel = tk.Label(leftframe, text=version, justify=tk.LEFT)
        versionlabel.place(x=1, y=1, anchor=tk.NW)

        self.header_string = "Finishing Up!"

        self.top_string = ("You're done! Check out the information below and make sure it's correct. When you hit the Export button, the new team member will be added to jump.db")
        

        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont",10), wraplength=500)
        # Proof
        report = tk.Frame(self)
        report.grid(row=3, column=0, sticky=tk.W+tk.E)
        self.proof = tk.Text(report, height=21, width=60)
        self.proof_scroll = tk.Scrollbar(report, orient=tk.VERTICAL)
        self.proof['yscrollcommand'] = self.proof_scroll.set
        self.proof_scroll['command'] = self.proof.yview
        self.proof_scroll.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)
        self.proof.insert(tk.END, "Name:\t" + user.firstname.title() + " " + user.lastname.title() + "\n")
        self.proof.insert(tk.END, "Phone:\t" + user.phone + "\n")
        self.proof.insert(tk.END, "Personal Email:\t" + user.email + "\n")
        self.proof.insert(tk.END, "JumpVisual Email:\t" + user.jvemail + "\n")
        self.proof.insert(tk.END, "Address:\t" + user.address + "\n")
        self.proof.insert(tk.END, "City:\t" + user.hometown + ", " + user.homestate+ "\n")
        self.proof.insert(tk.END, "Birthday:\t" + user.birthday + "\n")
        self.proof.insert(tk.END, "FAA Cert#:\t" + user.faa_num + "\n")
        self.proof.insert(tk.END, "Services:\t" + user.abilities + "\n")
        self.proof.insert(tk.END, "Emergency Contact:\t{x} ({y}) {z}\n".format(x=user.emer_name, y=user.emer_relation, z=user.emer_cell))
        self.proof.insert(tk.END, "### COVERAGE ZONE ###\n")
        self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns
        
        for town in self.usertowns:
            self.proof.insert(tk.END, town + "\n")
        self.proof.config(state=tk.DISABLED)
        self.proof.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        nav = tk.Frame(self)
        nav.grid(row=5, column=0, sticky=tk.E)
        
        self.finlabelgood = tk.Label(report, fg="GREEN", text="Team Member succesfully added to database", anchor=tk.W)
        self.finlabelbad = tk.Label(report, fg="RED", text="Uh oh! Something went wrong!", anchor=tk.W)

        self.export_button = ttk.Button(report, text="Export", command=lambda:self.next(user))
        self.export_button.grid(row=2, column=1, sticky=tk.E, pady=10)
        

        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, columnspan=2, ipady=8)
        
    def next(self, user):
        try:
            writeNewGuy(user)
            self.finlabelgood.grid(row=2, column=0, sticky=tk.W)
        except:
            self.finlabelbad.grid(row=2, column=0, sticky=tk.W)
            
    
def writeNewGuy(user):
    with conn:
        c.execute("INSERT INTO photographers (first, last, phone, email, jv_email, address, city, state, zip, birthday, faa_num, abilities, emer_name, emer_rel, emer_cell) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.firstname, user.lastname, user.phone, user.email, user.jvemail, user.address,  user.hometown, user.homestate, user.zip, user.birthday, user.faa_num, user.abilities, user.emer_name, user.emer_relation, user.emer_cell))
        conn.commit()

    # c.execute("SELECT employee_ID FROM photographers WHERE first=? AND last=?", (user.firstname, user.lastname))
    # photoID = c.fetchone()
    # photoID = str(photoID[0])
    # print("ID of new guy is " + str(photoID))

        
### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        ##print("A user has been created")
        self.firstname = ''
        self.lastname = ''
        self.email = ''
        self.jvemail = ''
        self.phone = ''
        self.address = ''
        self.hometown = ''
        self.homestate = 'NJ'
        self.abilities = ''
        self.birthday = '' #m/d
        self.zip = ''
        self.faa_num = 'None'
        self.nj_bool = False
        self.ny_bool = False
        self.man_bool = False
        self.ct_bool = False
        self.nj_counties = []
        self.ny_counties = []
        self.ct_counties = []
        self.nj_towns = []
        self.ny_towns = []
        self.ct_towns = []
        self.emer_name = ''
        self.emer_relation = ''
        self.emer_cell = ''
        


def choose_frames(user):
    """appends frames for appropriate states"""
    ##print(self.frames)
    if user.nj_bool:
        frames.append(NJCounties)
        frames.append(NJTowns)
    if user.ny_bool:
        frames.append(NYCounties)
        frames.append(NYTowns)
    if user.ct_bool:
        frames.append(CTCounties)
        frames.append(CTTowns)

    frames.append(FinalFrame)   
    limit = len(frames)
    ##print(self.frames)

        
def resetAll():
    window.destroy()
    global i
    i = 0

def run(): 
    global user
    user = User()

    checkjumpdb()

    global window
    window = tk.Toplevel()
    window.title("JumpWizard")
    window.wm_iconbitmap('jvdb.ico')
    #window.wm_iconbitmap('jwicon.ico')
    window.title("JumpVisual Photographer Coverage Wizard")
    window.resizable(width=False, height=False)
    window.protocol("WM_DELETE_WINDOW", resetAll)
    global baseimage
    baseimage = tk.PhotoImage(file="jump.pbm") 

    global njimage
    njimage = tk.PhotoImage(file="s_nj.pbm")

    global nyimage
    nyimage = tk.PhotoImage(file="s_ny.pbm")

    global ctimage
    ctimage = tk.PhotoImage(file="s_ct.pbm")

    global frames
    frames = [Frame2]

    global limit
    limit = len(frames)

    global leftframe
    leftframe = tk.Frame(window, width=600)
    leftframe.grid(row=0, column=0, sticky='news', rowspan=4)

    global sidebar
    sidebar = tk.Label(leftframe, image=baseimage)
    sidebar.image = baseimage
    sidebar.grid(row=0, column=0, sticky='ns')

    global current_frame
    current_frame = frames[i](window, user, padx=30, pady=30, width=400)
    #current_frame.grid(row=0,column=1)

    #version
    global versionlabel
    versionlabel = tk.Label(leftframe, text=version, justify=tk.LEFT)
    versionlabel.place(x=1, y=1, anchor=tk.NW)

    #styling
    window.grid_propagate(True) 
    leftframe.rowconfigure(0, weight=1)
    leftframe.columnconfigure(0, weight=0)
    window.rowconfigure(1, weight=1)
    drawframe(user)
    

def drawframe(user):
    """draws current frame""" 
    #print("i is " + str(i) + " limit is " + str(self.limit))
    current_frame = frames[i](window, user, padx=30, pady=30, width=400)        
    current_frame.grid(row=0,column=1)

def next_frame(current_frame):
    """advances to next frame."""
    current_frame.destroy()
    global i
    i += 1
    drawframe(user)

def prev_frame(current_frame):
    """returns to previous frame"""
    current_frame.destroy()
    global i
    i -= 1
    drawframe(user)

    



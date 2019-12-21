import tkinter as tk
import sqlite3
import os

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
    'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'sommerset', 'sussex', 'union', 'warren')

ny_counties = ('albany', 'allegany', 'bronx', 'broome', 'cattaraugus', 'cayuga', 'chautauqua', 'chemung', 'chenango', 'clinton', 'columbia', 'cortland', 'delaware',
               'dutchess', 'erie', 'essex', 'franklin', 'fulton', 'genesee', 'greene', 'hamilton', 'herkimer', 'jefferson', 'kings', 'lewis', 'livingston', 'madison',
               'monroe', 'montgomery', 'nassau', 'new york', 'niagra', 'oneida', 'onondaga', 'ontario', 'orange', 'orleans', 'oswego', 'otsego', 'putnam', 'queens',
               'rensselaer', 'richmond', 'rockland', 'st. lawrence', 'saratoga', 'schenectady', 'schoharie', 'schuyler', 'seneca', 'steuben', 'suffolk', 'sullivan',
               'tioga', 'tompkins', 'ulster', 'warren', 'washington', 'wayne', 'westchester', 'wyoming', 'yates')

ct_counties = ('fairfield', 'hartford', 'litchfield', 'middlesex', 'new haven', 'new london', 'tolland', 'windham')

### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        firstname = ''
        lastname = ''
        email = ''
        phone = ''
        hometown = ''
        homestate = 'NJ'
        jvemail = ''
        abilities = ''
        nj_bool = False
        ny_bool = False
        man_bool = False
        ct_bool = False
        nj_counties = []
        ny_counties = []
        ct_counties = []
        nj_towns = []
        ny_towns = []
        ct_towns = []

class Frame1(tk.Frame):

    def __init__(self, parent, User, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 1"
        self.top_string = ("Let's first fill out your profile. Enter your name, contact information, and the services you provide.")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        info = tk.Frame(self)
        info.grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
        tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="Phone Number").grid(row=2, column=0, sticky=tk.W)
        tk.Label(info, text="Email").grid(row=2, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="City of Residence").grid(row=4, column=0, sticky=tk.W)
        tk.Label(info, text="State").grid(row=4, column=1, sticky=tk.W, padx=20)
        tk.Label(info, text="JumpVisual Email").grid(row=7, column=0, sticky=tk.W)
        
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
        self.choices=[ 'NJ', 'NY', 'CT', 'PA' ]
        self.statevar = tk.StringVar()
        self.statepulldown = ttk.OptionMenu(info, self.statevar, self.choices[1], *self.choices)
        self.city_entry.grid(row=5, column=0, sticky=tk.W)
        self.statepulldown.grid(row=5, column=1, sticky=tk.W, padx=20)
        self.statevar.set(user.homestate)
        
        self.jvemail = tk.StringVar()
        self.jvemail.set(user.jvemail)
        self.jvemail_entry = tk.Entry(info, textvariable=self.jvemail)
        self.jvemail_entry.grid(row=8, column=0, sticky=tk.W)
                  
        states = tk.Frame(self, pady=10)
        states.grid(row=4, column=0, sticky=tk.W)
        tk.Label(states, text="What areas does your coverage zone include?").grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.njvar = tk.IntVar()
        self.njvar.set(user.nj_bool)
        self.njbox = tk.Checkbutton(states, text='NJ', variable=self.njvar)
        self.njbox.grid(row=1, column=0, sticky=tk.W)
        self.nyvar = tk.IntVar()
        self.nyvar.set(user.ny_bool)
        self.nybox = tk.Checkbutton(states, text='NY', variable=self.nyvar)
        self.nybox.grid(row=1, column=1, sticky=tk.W, padx=10)
        self.ctvar = tk.IntVar()
        self.ctvar.set(user.ct_bool)
        self.ctbox = tk.Checkbutton(states, text='CT', variable=self.ctvar)
        self.ctbox.grid(row=1, column=2, sticky=tk.W, padx=10)
        
        services = tk.Frame(self,pady=2, bd=1, relief=tk.GROOVE)
        services.grid(row=7, column=0, sticky=tk.W)
        tk.Label(self, text="Additional Services You Offer").grid(row=5, column=0, columnspan=3, sticky=tk.W)
        self.weekendsvar = tk.IntVar()
        if "WkEnds/" in user.abilities:
            self.weekendsvar.set(1)
        tk.Checkbutton(services, text='Work Weekends', variable=self.weekendsvar).grid(row=1, column=0, sticky=tk.W)
        self.floorvar = tk.IntVar()
        if "FP/" in user.abilities:
            self.floorvar.set(1)
        tk.Checkbutton(services, text='Floorplans', variable=self.floorvar).grid(row=2, column=0,sticky=tk.W)
        self.matvar = tk.IntVar()
        if "Vmatter/" in user.abilities:
            self.matvar.set(1)
        tk.Checkbutton(services, text='Matterport', variable=self.matvar).grid(row=3, column=0,sticky=tk.W)
        self.duvar = tk.IntVar()
        if "Pdusk/" in user.abilities:
            self.duvar.set(1)
        tk.Checkbutton(services, text='Dusk Photography', variable=self.duvar).grid(row=4, column=0, sticky=tk.W)
        self.aesvar = tk.IntVar()
        if "Paerial/" in user.abilities:
            self.aesvar.set(1)
        tk.Checkbutton(services, text='Aerial stills', variable=self.aesvar).grid(row=5, column=0,sticky=tk.W)
        self.faavar = tk.IntVar()
        if "FAA/" in user.abilities:
            self.faavar.set(1)
        tk.Checkbutton(services, text='FAA Certified', variable=self.faavar).grid(row=6, column=0,sticky=tk.W)
        
        tk.Label(services, text="Video Services:").grid(row=1, column=1, sticky=tk.W, padx=10)
        videoframe = tk.Frame(services, borderwidth=0, relief=tk.GROOVE)
        videoframe.grid(row=2, column=1, sticky=tk.W, rowspan=7,padx=10)
        self.teaservar = tk.IntVar()
        if "Vteaser/" in user.abilities:
            self.teaservar.set(1)
        tk.Checkbutton(videoframe, text="Teaser Video", variable=self.teaservar).grid(row=0, column=0, padx=25, sticky=tk.W)
        self.premvar = tk.IntVar()
        if "Vpremium/" in user.abilities:
            self.premvar.set(1)
        tk.Checkbutton(videoframe, text="Premium Video", variable=self.premvar).grid(row=1, column=0, padx=25, sticky=tk.W)
        self.luxvar = tk.IntVar()
        if "Vluxury/" in user.abilities:
            self.premvar.set(1)
        tk.Checkbutton(videoframe, text="Luxury Video", variable=self.luxvar).grid(row=2, column=0, padx=25, sticky=tk.W)
        self.aevvar = tk.IntVar()
        if "Vaerial/" in user.abilities:
            self.aevvar.set(1)
        tk.Checkbutton(videoframe, text='Aerial video', variable=self.aevvar).grid(row=3, column=0, padx=25,sticky=tk.W)
        self.veditvar = tk.IntVar()
        if "Vediting/" in user.abilities:
            self.veditvar.set(1)
        tk.Checkbutton(videoframe, text="Video Editing", variable=self.veditvar).grid(row=4, column=0, padx=25, sticky=tk.W)
        
        
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
        self.top_string_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, ipady=8)
        
        
    def nxt(self, user):
        user.firstname = self.fname_entry.get()
        user.lastname = self.lname_entry.get()
        user.nj_bool = self.njvar.get()
        user.ny_bool = self.nyvar.get()
#        user.man_bool = self.manvar.get()
        user.ct_bool = self.ctvar.get()
        user.phone = self.phone.get()
        user.email = self.email.get()
        user.jvemail = self.jvemail.get()
        user.hometown = self.city.get().rstrip('\n')
        user.homestate = self.statevar.get()
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
        if user.firstname == "" or user.lastname == "" or user.phone == "" or user.email == "" or user.hometown == "":
            tk.Label(self, text="You must fill out all info above to proceed!", fg="red").grid(row=3, column=0, sticky=tk.W)
        elif not user.nj_bool and not user.ny_bool and not user.ct_bool:
            tk.Label(self, text="You must check at lease one state!", fg="red").grid(row=6, column=0, sticky=tk.W)
        else:
           #print (user.firstname)
            app.choose_frames(user)
            app.next_frame(app.current_frame, app.i)
        
        
def newGuy():
    conn = sqlite3.connect('jump.db')
    global c 
    c = conn.cursor()
    global user
    user = User()
    frames = [Frame1]
    limit = len(frames)
    i = 0
    addwin = tk.Toplevel()
    addwin.title("Add a New Photographer")
    tk.Button(addwin, text="hello").grid(row=0, column=0)
    current_frame = frames[i](addwin, user, padx=30, pady=30, width=400)
    baseimage = tk.PhotoImage(file="jump.pbm")
    
    def drawframe(self, i, user):
        """draws current frame"""
        
        current_frame = frames[i](addwin, user, padx=30, pady=30, width=400)        
        current_frame.grid(row=0,column=1)
        
    drawframe(i, user)

    def choose_frames(self, user):
        """appends frames for appropriate states"""
        ##print(self.frames)
        self.frames = [Frame1, Frame2]
        if user.nj_bool:
            self.frames.append(NJCounties)
            self.frames.append(NJTowns)
        if user.ny_bool:
            self.frames.append(NYCounties)
            self.frames.append(NYTowns)
        if user.ct_bool:
            self.frames.append(CTCounties)
            self.frames.append(CTTowns)

        self.frames.append(FinalFrame)   
        self.limit = len(self.frames)
        ##print(self.frames)
        

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
        """writes .jmp file"""
        filename = user.firstname.title() + user.lastname.title() + '.jmp'

        self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns

        file = open(os.path.join(PATH, filename), 'w')
        file.write("#\tTo edit your contact info or coverage, you can run the wizard\n#\tagain or make changes to this file directly using Notepad (win)\n#\tor Textedit (mac). ")
        file.write("DO NOT add towns to this list that did not\n#\tappear in the wizard. Please notify johngallino@gmail.com or\n#\t@gallino on Slack about any missing towns.\n")
        file.write(user.firstname + " " + user.lastname + "\n")
        file.write(user.phone + "\n")
        file.write(user.email + "\n")
        file.write(user.hometown + " " + user.homestate + "\n")
        file.write(user.jvemail + "\n")
        file.write(user.abilities + "\n")
        for line in (set(user.nj_towns)):
            file.write(line + "\n")
        for line in (set(user.ny_towns)):
            file.write(line + "\n")
        for line in (set(user.ct_towns)):
            file.write(line + "\n")
        file.close()

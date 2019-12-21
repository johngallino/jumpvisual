import tkinter as tk
from tkinter import ttk
import config
import os
import otherframes

found = os.path.isfile('jump.db')

def parsePhone(phone):
    """ takes whatever fucked up phone number and formats it nice """
    numbers = ""
    for char in phone:
        if char.isdigit():
            numbers += char
    newphone = "(" + numbers[:3] + ') ' + numbers[3:6] + '-' + numbers[6:]
    return newphone

### FIRST SCREEN
class InfoFrame(tk.Frame):

    def __init__(self, parent, user,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.header_string = "Step 1"

        if not found:
            tk.Label(self, text="Uh oh! Can't find the jump.db file. Please place it in the same folder as the .exe file and start the program again.", fg="RED", wraplength=300).grid(row=3, column=0, sticky='ew')
            
        self.top_string = ("Enter the name, contact information, services provided by the new photographer.")
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
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, parent))
  
        
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        if not found:
            tk.Label(self, text="Uh oh! Can't find the jump.db file. Please place it in the same folder as the .exe file and start the program again.",
                     fg="RED", wraplength=300).grid(row=9, column=0, sticky='ew')
            self.next_button.destroy()
        #back button
#        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
#        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

    def drawnext(self, parent, user):
        win = parent
        config.current_frame = otherframes.frames[0](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)

    def choose_frames(self, user, parent):
            """appends frames for appropriate states"""
            ##print(self.frames)
            frames = otherframes.frames
            frames.clear()
            if user.nj_bool:
                frames.append(otherframes.NJCounties)
                frames.append(otherframes.NJTowns)
            if user.ny_bool:
                frames.append(otherframes.NYCounties)
                frames.append(otherframes.NYTowns)
            if user.ct_bool:
                frames.append(otherframes.CTCounties)
                frames.append(otherframes.CTTowns)   
            frames.append(otherframes.FinalFrame)   
            
            self.drawnext(parent, user)
        
    def nxt(self, user, parent):
        user.firstname = self.fname_entry.get().rstrip().title()
        user.lastname = self.lname_entry.get().rstrip().title()
        user.nj_bool = self.njvar.get()
        user.ny_bool = self.nyvar.get()
#        user.man_bool = self.manvar.get()
        user.ct_bool = self.ctvar.get()
        user.phone = parsePhone(self.phone.get())
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
        if user.firstname == '' or user.lastname == '':
            tk.Label(self, text="You must fill out name, phone, email, & city to proceed!", fg="red").grid(row=5, column=0, sticky=tk.W)
        
        elif not user.nj_bool and not user.ny_bool and not user.ct_bool:
            tk.Label(self, text="You must check at lease one state!", fg="red").grid(row=6, column=0, sticky=tk.W)
        else:
            self.choose_frames(user, parent)


    
            
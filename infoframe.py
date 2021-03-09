import tkinter as tk
from tkinter import ttk
import config

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
        
        
        #Error message
        self.error = tk.Label(self, text="error goes here", fg="red")

        nav = tk.Frame(self)
        nav.grid(row=8, column=0, sticky=tk.E + tk.S)
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, parent))
  
        
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        #back button
#        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:prev_frame(current_frame))
#        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

    def drawnext(self, parent, user):
        config.i += 1
        print('i is', str(config.i))
        config.drawframe(parent, user)


    def choose_frames(self, user, parent):
            """appends frames for appropriate states"""
            config.frames = ['infoframe']

            if user.nj_bool:
                config.frames.append('njcounties')
                config.frames.append('njtowns')
                # config.frames.append(countyframe.CountyFrame(parent, user, 'NJ'))
                # config.frames.append(townframe.TownFrame(parent, user, 'NJ'))
            if user.ny_bool:
                config.frames.append('nycounties')
                config.frames.append('nytowns')
                # config.frames.append(otherframes.NYCounties)
                # config.frames.append(otherframes.NYTowns)
            if user.ct_bool:
                config.frames.append('ctcounties')
                config.frames.append('cttowns')
                # config.frames.append(otherframes.CTCounties)
                # config.frames.append(otherframes.CTTowns)   
            config.frames.append('finalframe')
            # config.frames.append(finalframe.FinalFrame)   
            self.drawnext(parent, user)
        
    def nxt(self, user, parent):

        ### ENTRY VALIDATION
        if len(self.fname_entry.get()) == 0 or len(self.lname_entry.get()) == 0: # Name cannot be blank
            self.error.config(text="You must fill out the name field to proceed")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.fname_entry.get()) > 20 or len(self.lname_entry.get()) > 50: # Name length check
            self.error.config(text="Name is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)
        
        elif not self.fname_entry.get().isalpha() or not self.lname_entry.get().isalpha(): # Invalid characters in name field
            self.error.config(text="Name cannot contain spaces, numbers, or symbols")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.address.get()) > 50: # Address length check
            self.error.config(text="Address is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.phone.get()) > 14: # Phone length check
            self.error.config(text="Phone number is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.city.get()) > 30: # City length check
            self.error.config(text="City name is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.zip.get()) > 5: # Zip code length check
            self.error.config(text="Zip code is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.email.get()) > 25 or len(self.jvemail.get()) >25: # email length check
            self.error.config(text="Email address is too long!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.email.get()) > 0 and (not '@' in self.email.get() or not '.' in self.email.get()): # email must contain @ symbol
            self.error.config(text="Invalid email address")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.birthday.get()) > 5: # Birthday length check
            self.error.config(text="Birthday must be in MM/DD format")
            self.error.grid(row=5, column=0, sticky=tk.W)

        elif len(self.faa_num.get()) > 6: # FAA length check
            self.error.config(text="FAA Certification # is too long")
            self.error.grid(row=5, column=0, sticky=tk.W)
        
        elif not self.njvar.get() and not self.nyvar.get() and not self.ctvar.get(): # Must check at least one state
            self.error.config(text="You must check at least one state!")
            self.error.grid(row=5, column=0, sticky=tk.W)

        ### END VALIDATION
        else:
            # If all looks good, write data to user object
            user.firstname = self.fname_entry.get().rstrip().title()
            user.lastname = self.lname_entry.get().rstrip().title()
            user.nj_bool = self.njvar.get()
            user.ny_bool = self.nyvar.get()
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

            self.choose_frames(user, parent)

        


    
            
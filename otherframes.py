import tkinter as tk
from tkinter import ttk
import config
import jumpvisualdb as j
import wizardpop as w
import infoframe

i = 0
frames = []
limit = len(frames)

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
    'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'somerset', 'sussex', 'union', 'warren')

ny_counties = ('albany', 'allegany', 'bronx', 'broome', 'cattaraugus', 'cayuga', 'chautauqua', 'chemung', 'chenango', 'clinton', 'columbia', 'cortland', 'delaware',
               'dutchess', 'erie', 'essex', 'franklin', 'fulton', 'genesee', 'greene', 'hamilton', 'herkimer', 'jefferson', 'kings', 'lewis', 'livingston', 'madison',
               'monroe', 'montgomery', 'nassau', 'new york', 'niagra', 'oneida', 'onondaga', 'ontario', 'orange', 'orleans', 'oswego', 'otsego', 'putnam', 'queens',
               'rensselaer', 'richmond', 'rockland', 'st. lawrence', 'saratoga', 'schenectady', 'schoharie', 'schuyler', 'seneca', 'steuben', 'suffolk', 'sullivan',
               'tioga', 'tompkins', 'ulster', 'warren', 'washington', 'wayne', 'westchester', 'wyoming', 'yates')

ct_counties = ('fairfield', 'hartford', 'litchfield', 'middlesex', 'new haven', 'new london', 'tolland', 'windham')

class NJCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        #print("User abilities are saved as " + user.abilities)
        #print("next frame is " + str(frames[i+1]))
        njimage = tk.PhotoImage(file='graphics/s_nj.pbm')
        w.baseimage = njimage
        win = parent
        
        self.header_string = "Step 2 - New Jersey Counties"
        self.top_string = ("Next we are going to review the counties in the states selected as part of the photographer's coverage zone. Please select the counties that the photographer's coverage zone extends into. \n\nNOTE: checking a county below does NOT necessarily mean covering the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NJ Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Photographer's Zone:").grid(row=0, column=3, sticky=tk.W)
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

        if len(user.nj_counties) != 0:
            for county in user.nj_counties:
                self.userlistbox.insert(tk.END, county.title())
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
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
        
    def nxt(self, user, win):
        ##print(user.nj_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)

    def back(self, user, win):
        ##print(user.nj_counties)
            config.current_frame = infoframe.InfoFrame(win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)
            
            
        

class NJTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        win = parent
        #print("next frame is " + str(frames[i+1]))
        self.header_string = "Step 3 - NJ Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to the photographer's coverage zone.\n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
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
        state = "New Jersey"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        
        for town in holder:
            self.townbox.insert(tk.END, town.title())
 
        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        tk.Button(transfer, text="Add Whole County", command=lambda:self.add_wholeCounty(user)).grid(row=5, column=0, padx=20)
        
        ### USER BOX
        tk.Label(transfer, text="Your NJ Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=21, width=25, selectmode=tk.EXTENDED)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.nj_towns) != 0:
            for town in user.nj_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #tk.Label(nav, text="If you notice a town is missing, please notify @gallino").grid(row=0, column=0, sticky=tk.W)

        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_town(self, user):
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))
        user.nj_towns.append(self.townbox.get(tk.ACTIVE))
        self.townbox.delete(tk.ACTIVE)
        
    def add_wholeCounty(self, user):
        wholecounty = self.townbox.get(0,tk.END)
        #print(wholecounty)
        for i in range(len(wholecounty)):
            self.userlistbox.insert(tk.END, wholecounty[i])
            user.nj_towns.append(wholecounty[i])
            self.townbox.delete(0,tk.END)
        
            
    def del_town(self, user):
        user.nj_towns.remove(self.userlistbox.get(tk.ACTIVE))
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        self.userlistbox.delete(tk.ACTIVE)
        
        
    def view_towns(self):
        self.townbox.delete(0, tk.END) # clear
        county = self.njlistbox.get(tk.ACTIVE)
        state = "New Jersey"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user, win):
        ##print(user.nj_counties)
        ##print(user.nj_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)

    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)
        
### NY COUNTIES
class NYCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        #print("next frame is " + str(frames[i+1]))
        win = parent
        config.imgpath = 'graphics/s_ny.pbm'
        
        self.header_string = "Step 2 - New York Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of the photographer's coverage zone. Please select the counties that the photographer's coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="NY Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Photographer's Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
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
        
        if len(user.ny_counties) != 0:
            for county in user.ny_counties:
                self.userlistbox.insert(tk.END, county.title())
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
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
        
    def nxt(self, user, win):
        ##print(user.ny_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)

    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)
        
### NY TOWNS
class NYTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        img = tk.PhotoImage(file="graphics/s_ny.pbm") 
        self.header_string = "Step 3 - NY Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to the photographer's coverage zone. \n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16),justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        win = parent
        
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        #reset NY towns if there are any
#        if len(user.ny_towns) !=0:
#            user.ny_towns=[]
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### NY COUNTIES
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
        state = "New York"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        
        for town in holder:
            self.townbox.insert(tk.END, town.title())
            
        
      
        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        
        ### USER BOX
        tk.Label(transfer, text="Your NY Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=21, width=25, selectmode=tk.EXTENDED)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.ny_towns) != 0:
            for town in user.ny_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
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
        state = "New York"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user, win):
        ##print(user.ny_counties)
        ##print(user.ny_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)

    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)
            
## CONNECTICUT            
class CTCounties(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ##print("User abilities are saved as " + user.abilities)
        win = parent
        self.header_string = "Step 2 - Connecticut Counties"
        self.top_string = ("Next we are going to review the counties in the states that you selected as part of the photographer's coverage zone. Please select the counties that the photographer's coverage zone extends into. \n\nNOTE: checking a county below does NOT mean you have to cover the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)
        #print("next frame is " + str(frames[i+1]))
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text="CT Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Photographer's Zone:").grid(row=0, column=3, sticky=tk.W)
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
        
        if len(user.ct_counties) != 0:
            for county in user.ct_counties:
                self.userlistbox.insert(tk.END, county.title())
        
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user,win))
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
        
    def nxt(self, user, win):
        ##print(user.ct_counties)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)
    
    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)

class CTTowns(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        win = parent
        #print("next frame is " + str(frames[i+1]))
        self.header_string = "Step 3 - CT Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to the photographer's coverage zone. \n\nPulling up a map is highly recommended for this part!")
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

        ### CT COUNTIES
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
        state = "Connecticut"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        
        for town in holder:
            self.townbox.insert(tk.END, town.title())
            
        
      
        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        
        ### USER BOX
        tk.Label(transfer, text="Your CT Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=21, width=25, selectmode=tk.EXTENDED)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        if len(user.ct_towns) != 0:
            for town in user.ct_towns:
                self.userlistbox.insert(tk.END, town.title())
                
        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
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
        state = "Connecticut"
        j.c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_name=?", (county, state))
        holder = [tup[0] for tup in j.c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    def nxt(self, user, win):
        ##print(user.ct_counties)
        ##print(user.ct_towns)
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            global i
            i += 1
            config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
            config.current_frame.grid(row=0,column=1)

    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)
        
class FinalFrame(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #update sidebar
        win = parent
        self.header_string = "Finishing Up!"

        self.top_string = ("You're done! Check out the information below and make sure it's correct. When you hit the Confirm button, the new team member will be added to jump.db")
        

        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont",10), wraplength=500)
        # Proof
        report = tk.Frame(self)
        report.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.proof = tk.Text(report, height=21, width=60)
        self.proof.tag_configure('proof', font='TKDefaultFont 10', lmargin1=3, justify='left')
        self.proof_scroll = tk.Scrollbar(report, orient=tk.VERTICAL)
        self.proof['yscrollcommand'] = self.proof_scroll.set
        self.proof_scroll['command'] = self.proof.yview
        self.proof_scroll.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)
        self.proof.insert(tk.END, "Name:\t" + user.firstname.title() + " " + user.lastname.title() + "\n", 'proof')
        self.proof.insert(tk.END, "Phone:\t" + user.phone + "\n", 'proof')
        self.proof.insert(tk.END, "Personal Email:\t" + user.email + "\n", 'proof')
        self.proof.insert(tk.END, "JumpVisual Email:\t" + user.jvemail + "\n", 'proof')
        self.proof.insert(tk.END, "Address:\t" + user.address + "\n", 'proof')
        self.proof.insert(tk.END, "City:\t" + user.hometown + ", " + user.homestate+ "\n", 'proof')
        self.proof.insert(tk.END, "Birthday:\t" + user.birthday + "\n", 'proof')
        self.proof.insert(tk.END, "FAA Cert#:\t" + user.faa_num + "\n", 'proof')
        self.proof.insert(tk.END, "Services:\t" + user.abilities + "\n", 'proof')
        self.proof.insert(tk.END, "Emergency Contact:\t{x} ({y}) {z}\n".format(x=user.emer_name, y=user.emer_relation, z=user.emer_cell), 'proof')
        self.proof.insert(tk.END, "\n### COVERAGE ZONE ###\n", 'proof')
        self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns
        
        for town in self.usertowns:
            self.proof.insert(tk.END, town + "\n", 'proof')
        self.proof.config(state=tk.DISABLED)
        self.proof.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        nav = tk.Frame(self)
        nav.grid(row=5, column=0, sticky=tk.E)
        
        self.finlabelgood = tk.Label(report, fg="GREEN", text="Team Member successfully added to database! You may now close this wizard.", anchor=tk.W)
        self.finlabelbad = tk.Label(report, fg="RED", text="Uh oh! Something went wrong!", anchor=tk.W)

        self.export_button = ttk.Button(report, text="Confirm New Photographer", command=lambda:self.export(user))
        self.export_button.grid(row=2, column=1, sticky=tk.E, pady=10, ipadx=10)
        
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, columnspan=2, ipady=8)
        
    def export(self, user):
        try:
            w.writeNewGuy(user)
            self.finlabelgood.grid(row=2, column=0, sticky=tk.W)
        except IOError:
            print("Error: problem writing data to file")
            self.finlabelbad.grid(row=2, column=0, sticky=tk.W)
        except ValueError:
            print('Error: problem with the data entered')
        except:
            print("Error: some other error occured")
            self.finlabelbad.grid(row=2, column=0, sticky=tk.W)
        finally:
            user.name = (user.firstname + ' ' + user.lastname).title()
            config.newuser = user.name


    def back(self, user, win):
        global i
        i -= 1
        config.current_frame = frames[i](win, user, padx=30, pady=30, width=400)
        config.current_frame.grid(row=0,column=1)
import tkinter as tk
from tkinter import ttk
import config
from jumpvisualdb import checkjumpdb

class TownFrame(tk.Frame):
    _STATE = ''
    _STATELONG = ''

    def __init__(self, parent, user, _STATE, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        win = parent
        #print("TownFrame created.")
        self._STATE = _STATE
        
        if _STATE == 'NJ': 
            self._STATELONG = 'New Jersey'
        elif _STATE == 'NY': 
            self._STATELONG = 'New York'
        elif _STATE == 'CT': 
            self._STATELONG = 'Connecticut'
        else: 
            self._STATELONG = 'ERROR'

        checkjumpdb()
        
        self.header_string = "Step 3 - " + _STATE + " Towns"
        self.top_string = ("Next we're going to select the towns inside of each county you selected. Select each county to view the towns in that county, then add the towns to the photographer's coverage zone.\n\nPulling up a map is highly recommended for this part!")
        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                  font=("TKDefaultFont", 16), justify="left", wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, anchor=tk.W,
                                     font=("TKDefaultFont", 10), justify="left", wraplength=500)
        
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        
        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0, columnspan=2)

        ### PHOTOGRAPHER'S COVERED COUNTIES BOX FOR GIVEN STATE
        tk.Label(transfer, text="Your " + _STATE + " Counties:").grid(row=0, column=0, sticky=tk.W)
        self.county_listbox = tk.Listbox(transfer, height=4, width=25)
        self.county_listbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.county_listbox['yscrollcommand'] = self.county_listbox_scroll.set
        self.county_listbox_scroll['command'] = self.county_listbox.yview
        

        #### TOWNS IN SELECTED COUNTY BOX
        tk.Label(transfer, text="Towns in Selected County:").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.townbox = tk.Listbox(transfer, height=15, width=25)
        self.townbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.townbox['yscrollcommand'] = self.townbox_scroll.set
        self.townbox_scroll['command'] = self.townbox.yview
        self.townbox.grid(row=3, column=0, rowspan=2, sticky=tk.W)
        self.townbox_scroll.grid(row=3, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E)

        ### TRANSFER BUTTONS
        tk.Button(transfer, text="View Towns", command=lambda:self.view_towns()).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_town(user)).grid(row=3, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_town(user)).grid(row=4, column=2,padx=20)
        tk.Button(transfer, text="Add Whole County", command=lambda:self.add_wholeCounty(user)).grid(row=5, column=0, padx=20)

        ### USER BOX OF COVERED TOWNS
        tk.Label(transfer, text="Your " + _STATE + " Coverage Zone:").grid(row=0, column=3, sticky=tk.W)
        self.userlistbox = tk.Listbox(transfer, height=20, width=25, selectmode=tk.EXTENDED)
        self.userlistbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
        self.userlistbox_scroll['command'] = self.userlistbox.yview

        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, win))
        self.next_button.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, win))
        self.back_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

        if self._STATE == 'NJ':
            for county in user.nj_counties:
                self.county_listbox.insert(tk.END, county.title())
                
            if len(user.nj_towns) != 0:
                for town in user.nj_towns:
                    self.userlistbox.insert(tk.END, town.title())
                    
        elif self._STATE == 'NY':
            for county in user.ny_counties:
                self.county_listbox.insert(tk.END, county.title())
                
            if len(user.ny_towns) != 0:
                for town in user.ny_towns:
                    self.userlistbox.insert(tk.END, town.title())
                    
        elif self._STATE == 'CT':
            for county in user.ct_counties:
                self.county_listbox.insert(tk.END, county.title())
                
            if len(user.ct_towns) != 0:
                for town in user.ct_towns:
                    self.userlistbox.insert(tk.END, town.title())
                    
        # RENDER POPULATED BOXES
        self.county_listbox.grid(row=1, column=0, rowspan=1, sticky=tk.W)
        self.county_listbox_scroll.grid(row=1, column=1, rowspan=1, sticky=tk.N+tk.S+tk.E)
        self.userlistbox.grid(row=1, column=3, rowspan=4, sticky=tk.W)
        self.userlistbox_scroll.grid(row=1, column=3, rowspan=4, sticky=tk.E+tk.N+tk.S)
        
        county = self.county_listbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_id=?", (county, self._STATE))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())
        
    ### CLASS METHODS
    
    def add_town(self, user):
        # Add a town to photographer's coverage
        self.userlistbox.insert(tk.END, self.townbox.get(tk.ACTIVE))

        if self._STATE == 'NJ':
            user.nj_towns.append(self.townbox.get(tk.ACTIVE))
        elif self._STATE == 'NY':
            user.ny_towns.append(self.townbox.get(tk.ACTIVE))
        elif self._STATE == 'CT':
            user.ct_towns.append(self.townbox.get(tk.ACTIVE))

        self.townbox.delete(tk.ACTIVE)
        
    def add_wholeCounty(self, user):
        # Add all towns in selected county to photographer's coverage
        wholecounty = self.townbox.get(0,tk.END)
        
        for i in range(len(wholecounty)):
            self.userlistbox.insert(tk.END, wholecounty[i])
            
            if self._STATE == 'NJ':
                user.nj_towns.append(wholecounty[i])
            elif self._STATE == 'NY':
                user.ny_towns.append(wholecounty[i])
            elif self._STATE == 'CT':
                user.ct_towns.append(wholecounty[i])

            self.townbox.delete(0,tk.END)

            
    def del_town(self, user):
        # Delete a town from photographer's coverage
        active = self.userlistbox.get(tk.ACTIVE)
        self.townbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))

        if self._STATE == 'NJ':
            for item in user.nj_towns:
                if active in item:
                    user.nj_towns.remove(item)
        elif self._STATE == 'NY':
            for item in user.ny_towns:
                if active in item:
                    user.ny_towns.remove(item)
        elif self._STATE == 'CT':
            for item in user.ct_towns:
                if active in item:
                    user.ct_towns.remove(item)

        self.userlistbox.delete(tk.ACTIVE)
            
    def view_towns(self):
        # Populate townbox with all towns for selected county
        self.townbox.delete(0, tk.END) 
        county = self.county_listbox.get(tk.ACTIVE)
        c.execute("SELECT upper(county_name) ||' | ' || city FROM UScities WHERE county_name=? AND state_id=?", (county, self._STATE))
        holder = [tup[0] for tup in c.fetchall()]
        holder.sort()
        for town in holder:
            self.townbox.insert(tk.END, town.title())

    def nxt(self, user, win):
        # Go to next frame in wizard
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one town to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            user.i += 1
            config.current_frame = config.frameController.frameSwitcher(user, win)
            config.current_frame.grid(row=0,column=1)
            
    def back(self, user, win):
        # Go back one frame in wizard
        user.i -= 1
        config.current_frame = config.frameController.frameSwitcher(user, win)
        config.current_frame.grid(row=0,column=1)
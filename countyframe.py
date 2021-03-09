import tkinter as tk
from tkinter import ttk
from jumpvisualdb import checkjumpdb
import inspect
import config

nj_counties = ('atlantic', 'bergen', 'burlington', 'camden', 'cape may', 'cumberland', 'essex', 'gloucester', 'hudson', 'hunterdon', 
    'mercer', 'middlesex', 'monmouth', 'morris', 'ocean', 'passaic', 'salem', 'somerset', 'sussex', 'union', 'warren')

ny_counties = ('albany', 'allegany', 'bronx', 'broome', 'cattaraugus', 'cayuga', 'chautauqua', 'chemung', 'chenango', 'clinton', 'columbia', 'cortland', 'delaware',
               'dutchess', 'erie', 'essex', 'franklin', 'fulton', 'genesee', 'greene', 'hamilton', 'herkimer', 'jefferson', 'kings', 'lewis', 'livingston', 'madison',
               'monroe', 'montgomery', 'nassau', 'new york', 'niagra', 'oneida', 'onondaga', 'ontario', 'orange', 'orleans', 'oswego', 'otsego', 'putnam', 'queens',
               'rensselaer', 'richmond', 'rockland', 'st. lawrence', 'saratoga', 'schenectady', 'schoharie', 'schuyler', 'seneca', 'steuben', 'suffolk', 'sullivan',
               'tioga', 'tompkins', 'ulster', 'warren', 'washington', 'wayne', 'westchester', 'wyoming', 'yates')

ct_counties = ('fairfield', 'hartford', 'litchfield', 'middlesex', 'new haven', 'new london', 'tolland', 'windham')

class CountyFrame(tk.Frame):
    _STATE = ''
    _STATELONG = ''

    def __init__(self, parent, user, _STATE, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #print("CountyFrame created.")
        self._STATE = _STATE
        checkjumpdb()
        if _STATE == 'NJ': 
            self._STATELONG = 'New Jersey'
            #parent.sidebar.config(image=parent.njimage)
        #     config.wizardpop.sidebar.grid(row=0, column=0, sticky='ns')
        # elif _STATE == 'NY': 
        #     self._STATELONG = 'New York'
        #     config.wizardpop.sidebar.config(image=config.wizardpop.nyimage)
        #     config.wizardpop.sidebar.grid(row=0, column=0, sticky='ns')
        # elif _STATE == 'CT': 
        #     self._STATELONG = 'Connecticut'
        #     config.wizardpop.sidebar.config(image=config.wizardpop.ctimage)
        #     config.wizardpop.sidebar.grid(row=0, column=0, sticky='ns')
        # else: 
        #     self._STATELONG = 'ERROR'

        self.header_string = "Step 2 - " + _STATE + " Counties"
        self.top_string = ("Next we are going to review the counties in the states selected as part of the photographer's coverage zone. Please select the counties that the photographer's coverage zone extends into. \n\nNOTE: checking a county below does NOT necessarily mean covering the entire county")
        self.header_label = tk.Label(self, text=self.header_string, justify="left", anchor=tk.W,
                                  font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont", 10), wraplength=500)

        transfer = tk.Frame(self)
        transfer.grid(row=2, column=0)
        nav = tk.Frame(self)
        nav.grid(row=4,column=0, sticky=tk.E, pady=10)
        tk.Label(transfer, text=_STATE +" Counties:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(transfer, text="Photographer's Zone:").grid(row=0, column=3, sticky=tk.W)
        self.listbox = tk.Listbox(transfer, height=21)
        self.listbox_scroll = tk.Scrollbar(transfer, orient=tk.VERTICAL)
        self.listbox['yscrollcommand'] = self.listbox_scroll.set
        self.listbox_scroll['command'] = self.listbox.yview

        self.listbox.grid(row=1, column=0, rowspan=2, sticky=tk.W)
        self.listbox_scroll.grid(row=1, column=1, rowspan=3, sticky=tk.N+tk.S+tk.E)
        tk.Button(transfer, text="  Add >>  ", command=lambda:self.add_county(user)).grid(row=1, column=2, padx=20)
        tk.Button(transfer, text="<< Remove", command=lambda:self.del_county(user)).grid(row=2, column=2,padx=20)
        self.userlistbox = tk.Listbox(transfer, height=21)

        if _STATE == 'NJ': 
            for county in nj_counties:
                self.listbox.insert(tk.END, county.title())
            if len(user.nj_counties) != 0:
                for county in user.nj_counties:
                    self.userlistbox.insert(tk.END, county.title())
        elif _STATE == 'NY': 
            for county in ny_counties:
                self.listbox.insert(tk.END, county.title())
            if len(user.ny_counties) != 0:
                for county in user.ny_counties:
                    self.userlistbox.insert(tk.END, county.title())
        elif _STATE == 'CT': 
            for county in ct_counties:
                self.listbox.insert(tk.END, county.title())
            if len(user.ct_counties) != 0:
                for county in user.ct_counties:
                    self.userlistbox.insert(tk.END, county.title())

        self.userlistbox.grid(row=1, column=3, rowspan=2, sticky=tk.W)

        #next button
        self.next_button = ttk.Button(nav, text="Next >>", command=lambda:self.nxt(user, parent))
        self.next_button.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, parent))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)


        #placing the widgets inside Frame3
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=8)

    def add_county(self, user):
        ''' add a county to photographer's coverage '''
        self.userlistbox.insert(tk.END, self.listbox.get(tk.ACTIVE))

        if self._STATE == 'NJ':
            user.nj_counties.append(self.listbox.get(tk.ACTIVE))
        elif self._STATE == 'NY':
            user.ny_counties.append(self.listbox.get(tk.ACTIVE))
        elif self._STATE == 'CT':
            user.ct_counties.append(self.listbox.get(tk.ACTIVE))

        self.listbox.delete(tk.ACTIVE)

    def del_county(self, user):
        ''' remove a county from photographer's coverage '''
        self.listbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
        if self._STATE == 'NJ':
            user.nj_counties.remove(self.userlistbox.get(tk.ACTIVE))
        elif self._STATE == 'NY':
            user.ny_counties.remove(self.userlistbox.get(tk.ACTIVE))
        elif self._STATE == 'CT':
            user.ct_counties.remove(self.userlistbox.get(tk.ACTIVE))

        self.userlistbox.delete(tk.ACTIVE)

    def nxt(self, user, parent):
        if self.userlistbox.get(0) == "":
            tk.Label(self, text="You must add at least one county to the photographer's coverage zone", fg="red").grid(row=3, column=0, sticky=tk.W+tk.E)
        else:
            config.i += 1
            config.drawframe(parent, user)

    def back(self, user, parent):
            config.i -= 1
            config.drawframe(parent, user)
        

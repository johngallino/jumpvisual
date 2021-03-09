import tkinter as tk
import infoframe
import countyframe
import townframe
import finalframe

imgpath = 'graphics/jump.pbm'
frames = ['infoframe']
i = 0

def drawframe(win, user):
    """draws wizardpop frame"""
    #print('frames[i] is', frames[i])
    if frames[i] == 'infoframe':
        current_frame = infoframe.InfoFrame(win, user, padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'njcounties':
        current_frame = countyframe.CountyFrame(win, user, 'NJ', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'njtowns':
        current_frame = townframe.TownFrame(win, user, 'NJ', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'nycounties':
        current_frame = countyframe.CountyFrame(win, user, 'NY', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'nytowns':
        current_frame = townframe.TownFrame(win, user, 'NY', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'ctcounties':
        current_frame = countyframe.CountyFrame(win, user, 'CT', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'cttowns':
        current_frame = townframe.TownFrame(win, user, 'CT', padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')
    elif frames[i] == 'finalframe':
        current_frame = finalframe.FinalFrame(win, user, padx=30, pady=30, width=400)
        current_frame.grid(row=0,column=1, sticky='nsew')


### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        #print("A user has been created")
        self.firstname = 'w'
        self.lastname = 'w'
        self.nickname = ''
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
        self.nj_bool = True
        self.ny_bool = True
        self.ct_bool = True
        self.nj_counties = []
        self.ny_counties = []
        self.ct_counties = []
        self.nj_towns = []
        self.ny_towns = []
        self.ct_towns = []
        self.emer_name = ''
        self.emer_relation = ''
        self.emer_cell = ''
        self.name = ''

newuser = ''
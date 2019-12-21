import tkinter as tk

currentframe = ''
imgpath = 'jump.pbm'

def access():
	print("accessed config.py")

### USER CLASS
class User():
    """A class to hold the User's data """
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)

        #print("A user has been created")
        self.firstname = ''
        self.lastname = ''
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
        self.name = ''

newuser = ''
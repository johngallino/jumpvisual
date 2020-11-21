import sqlite3
import os
import tkinter as tk
from tkinter import ttk
import config
import infoframe

found = os.path.isfile('jump.db')
c = 0 
name = ''

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

    

def writeNewGuy(user):
    with conn:
        c.execute("INSERT INTO photographers (first, last, phone, email, jv_email, address, city, state, zip, birthday, faa_num, abilities, emer_name, emer_rel, emer_cell) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.firstname, user.lastname, user.phone, user.email, user.jvemail, user.address,  user.hometown, user.homestate, user.zip, user.birthday, user.faa_num, user.abilities, user.emer_name, user.emer_relation, user.emer_cell))
        conn.commit()
    with conn:
        c.execute("SELECT employee_ID FROM photographers WHERE first=? AND last=?", (user.firstname, user.lastname))
        photoID = c.fetchone()
        photoID = str(photoID[0])
        print("ID of new photographer is " + str(photoID))
        print(user.nj_towns)
        if user.nj_towns:
            print("ADDING NJ TOWNS...")
            for town in user.nj_towns:
                #print('town is ' + town)
                gix = town.split(' | ')
                county = gix[0]
                city = gix[1]
                #print('county is ' + county)
                #print('city is ' + city)
                try:
                    c.execute("SELECT id FROM UScities WHERE state_id=? AND county_name=? AND city=?",('NJ', county.rstrip(), city.rstrip()))
                    townID = c.fetchone()
                    townID = str(townID[0])
                    #print('townID is ' + townID)
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (photoID, townID))
                except:
    # ERROR SHOULD BE LOGGED TO LOG FILE
                    print("Error with", "NJ |", county, "County", city)
            print("DONE.")
        if user.ny_towns:
            print("ADDING NY TOWNS...")
            for town in user.ny_towns:
                #print('town is ' + town)
                gix = town.split(' | ')
                county = gix[0]
                city = gix[1]
                #print('county is ' + county)
                #print('city is ' + city)
                try:
                    c.execute("SELECT id FROM UScities WHERE state_id=? AND county_name=? AND city=?",('NY', county.rstrip(), city.rstrip()))
                    townID = c.fetchone()
                    townID = str(townID[0])
                    #print('townID is ' + townID)
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (photoID, townID))
                except:
    # ERROR SHOULD BE LOGGED TO LOG FILE
                    print("Error with", "NY |", county, "County", city)
            print("DONE.")
        if user.ct_towns:
            print("ADDING CT TOWNS...")
            for town in user.ct_towns:
                #print('town is ' + town)
                gix = town.split(' | ')
                county = gix[0]
                city = gix[1]
                #print('county is ' + county)
                #print('city is ' + city)
                try:
                    c.execute("SELECT id FROM UScities WHERE state_id=? AND county_name=? AND city=?",('CT', county.rstrip(), city.rstrip()))
                    townID = c.fetchone()
                    townID = str(townID[0])
                    #print('townID is ' + townID)
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (photoID, townID))
                except:
    # ERROR SHOULD BE LOGGED TO LOG FILE
                    print("Error with", "CT |", county, "County", city)
            print("DONE.")
        conn.commit()




class Wizardpop(): 

    def __init__(self):
        checkjumpdb()
        user = config.User()
        self.window = tk.Toplevel()
        self.window.title("JumpWizard")
        self.window.wm_iconbitmap('graphics/jvdb.ico')
        self.window.wm_iconbitmap('graphics/jwicon.ico')
        self.window.title("JumpVisual Photographer Coverage Wizard")
        self.window.resizable(width=False, height=False)
        global win
        win = self.window # is this neccesary?

        self.baseimage = tk.PhotoImage(file='graphics/jump.pbm')
        self.njimage = tk.PhotoImage(file='graphics/s_nj.pbm')
        self.nyimage = tk.PhotoImage(file='graphics/s_ny.pbm')
        self.ctimage = tk.PhotoImage(file='graphics/s_ct.pbm')

        self.leftframe = tk.Frame(self.window, width=600)
        self.leftframe.grid(row=0, column=0, sticky='news', rowspan=4)
        
        self.sidebar = tk.Label(self.leftframe, image=self.baseimage)
        self.sidebar.grid(row=0, column=0, sticky='ns')

        #styling
        self.window.grid_propagate(True) 
        self.leftframe.rowconfigure(0, weight=1)
        self.leftframe.columnconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=1)
        
        config.frames = [infoframe.InfoFrame]
        
        def drawframe(user, i):
            """draws parent frame"""
            
            config.current_frame = infoframe.InfoFrame(win, user, padx=30, pady=30, width=400)
            # current_frame = frames[i](win, user, i, frames, padx=30, pady=30, width=400)
           
#            if type(config.current_frame) == NJCounties:
#                sidebar.image = njimage
#            elif config.current_frame == NYCounties:
#                sidebar.image = nyimage
#            elif config.current_frame == CTCounties:
#                sidebar.image = ctimage
#            else:
#                print("config.current_frame is not NJ, Ny, or CT")
#                sidebar.image = baseimage
#            sidebar.grid(row=0, column=0, sticky='ns')
            config.current_frame.grid(row=0,column=1)

        drawframe(user, i)
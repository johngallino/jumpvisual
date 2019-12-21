import sqlite3
import os
import tkinter as tk
from tkinter import ttk
import config
import infoframe
from otherframes import *

def access():
    print("accessed wizardpop")

found = os.path.isfile('jump.db')
c = 0 #global variable
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
        print("ID of new guy is " + str(photoID))
        print(user.nj_towns)
        for town in user.nj_towns:
            print('town is ' + town)
            gix = town.split(' | ')
            county = gix[0]
            city = gix[1]
            print('county is ' + county)
            print('city is ' + city)
            c.execute("SELECT id FROM UScities WHERE state_id=? AND county_name=? AND city=?",('NJ', county.rstrip(), city.rstrip()))
            townID = c.fetchone()
            townID = str(townID[0])
            print('townID is ' + townID)
            c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (photoID, townID))
            conn.commit()


 

class wizardpop(): 

    def __init__(self):
        checkjumpdb()
        user = config.User()
        window = self.window = tk.Toplevel()
        global win
        win = window
        window.title("JumpWizard")
        window.wm_iconbitmap('jvdb.ico')
        #window.wm_iconbitmap('jwicon.ico')
        window.title("JumpVisual Photographer Coverage Wizard")
        window.resizable(width=False, height=False)

        baseimage = tk.PhotoImage(file=config.imgpath)

        leftframe = tk.Frame(window, width=600)
        leftframe.grid(row=0, column=0, sticky='news', rowspan=4)

        sidebar = tk.Label(leftframe, image=baseimage)
        sidebar.image = baseimage
        sidebar.grid(row=0, column=0, sticky='ns')

        # current_frame = frames[i](win, user, i, padx=30, pady=30, width=400)
        # current_frame.grid(row=0,column=1)

        #styling
        window.grid_propagate(True) 
        leftframe.rowconfigure(0, weight=1)
        leftframe.columnconfigure(0, weight=0)
        window.rowconfigure(1, weight=1)
        
        frames = [infoframe.InfoFrame]
        limit = len(frames)
        
        def drawframe(user, i):
            """draws current frame"""
            config.current_frame = infoframe.InfoFrame(win, user, padx=30, pady=30, width=400)
            # current_frame = frames[i](win, user, i, frames, padx=30, pady=30, width=400)
            # if current_frame == NJCounties:
            #     sidebar.image = njimage        
            config.current_frame.grid(row=0,column=1)

        drawframe(user, i)
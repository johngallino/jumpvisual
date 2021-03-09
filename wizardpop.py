import sqlite3
import os
import tkinter as tk
from tkinter import ttk
import config


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

class Wizardpop(): 
    """ A class to hold the Add Photographer Wizard pop up window """

    def __init__(self):
        user = config.User()
        self.i = 0
        self.window = tk.Toplevel()
        
        self.window.title("JumpWizard")
        self.window.wm_iconbitmap('graphics/jvdb.ico')
        self.window.wm_iconbitmap('graphics/jwicon.ico')
        self.window.title("JumpVisual Photographer Coverage Wizard")
        self.window.resizable(width=False, height=False)
        global win
        win = self.window 
        print('wizardpop win is ' + str(type(win)))
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
        
        # Frame control
        config.drawframe(win, user)
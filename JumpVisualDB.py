import sqlite3
import os
import sys
import shutil
import logging
import tkinter as tk
import TkTreectrl as tree
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, date
import dateformat
import wizardpop as w


## Created by John Gallino
## December, 2018

# Last edited 2/25/2021

# KNOWN BUGS TO FIX AND STUFF TO ADD
#### Add a confirmation dialog if wizard window is closed on last screen without Exporting
#### Improve error handling and exceptions
#### Add unit testing
#### Allow for names with spaces or hyphens or capital letters mid-name like DePrima
#### Get log window to work
#### Sanitize the search input
#### DONE                   BIGGER FONTS
#### Redesign search results area
#### Reconfigure db to break up services
#### DONE                   Swap positions of Save and Delete in the Edit Photographer window
#### DONE                   Allow for full screen/window resize
#### Add STATUS field and sort by status
#### MORE BACKUPS per day
#### Pop up business card for photographer
#### DONE                   Make coverage export list multi-select

version = "version 4.3"

#Creating a logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log.txt", level=logging.DEBUG, format = LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()
logger.info("JumpVisual Dispatch %s" % version)


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
    width = 320
    height = 100
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def checkjumpdb():
    """see if jump.db file is present"""
    try: 
        open('jump.db')
    except:
        messagebox.showerror("Uh Oh!", "Cannot find jump.db file! Program must close!")
        logger.critical("Cannot find jump.db file")
        return
    else:
        global conn
        conn = sqlite3.connect('jump.db')
        global c 
        c = conn.cursor()

    status_exists = False

    while not status_exists:
        try:
            c.execute("SELECT status FROM photographers")
        except:
            print('Status field not found in photographers table. Adding it now...')
            c.execute('ALTER TABLE photographers ADD COLUMN status DEFAULT Active')
        else:
            status_exists = True
            

def backerupper():
    ''' creates backup files of the database once a day '''
    found = os.path.isfile('jump.db')
    path = 'backups'
    path2 = os.path.join(path, 'jump.db')
    today = str(date.today())
    now = str(datetime.now(tz=None))
    print(now)
    LIMIT = 30 #number of backup files to store

    if os.path.exists('backups'):
        gix = os.listdir('backups') # dir is your directory path
        number_files = len(gix)

        gix = gix[:number_files-LIMIT]

        for file in gix:
            os.remove('backups/'+file) 

    if found and not os.path.exists('backups/backup_' + today + '.db'):
        if not os.path.exists('backups'):
            os.mkdir(path, 0o777)
            print("backups folder created")
        shutil.copy2('jump.db', path2)
        os.rename('backups/jump.db', ('backups/backup_' + today + '.db' ))
        print("Made a backup jump.db for today in backups folder")
        logger.info("Made a backup jump.db for today in backups folder")
        return True
    else:
        print("A backup of jump.db has already been made for today")
        logger.info("A backup of jump.db has already been made for today")
        return False
    
### ROOT SCREEN
class root(tk.Tk):
    """ JumpVisual Dispatch root window """

    def wizard(self):
        '''opens the New Guy/Gal wizard screen'''
        wizardpop = w.Wizardpop()
        app.wait_window(wizardpop.window)
        wizardpop.window.destroy()
        # clear rosterlist and repopulate it
        self.rosterbox.delete('ALL')
        global c
        c.execute("SELECT first, last from Photographers")
        allguys = c.fetchall()
        theRoster = []
        for guy in allguys:
            name = str(guy[0] + ' ' + guy[1])
            status = str(guy[2])
            theRoster.append((status, name))

        for guy in sorted(theRoster):
            self.rosterbox.insert(tk.END, guy[0], guy[1])
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        checkjumpdb()
        backerupper()
      ##MAIN WINDOW  
        self.title("JumpVisual Dispatch Protocol " + version)
        self.configure(bg="WHITE")
        self.resizable(width=True, height=True)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(3,weight=1)
        self.columnconfigure(1, weight=1)
        self.wm_iconbitmap('graphics/jvdb.ico')
        self.p_abilities = ''
        self.p_notes = ''
        self.p_realtors = ''
    ## TOP IMAGE
        self.headimg = tk.PhotoImage(file="graphics/dispatch.pbm")
        self.banner = tk.Label(self,bg='white', image=self.headimg)
        self.banner.image = self.headimg
        self.banner.grid(row=0, column=0, columnspan=10, sticky='we')
        

    ## LEFT FRAME
        leftframe = tk.Frame(self, bg="WHITE")
        leftframe.grid(row=1, column=0, sticky='nwes', rowspan=2)
        leftframe.rowconfigure(1,weight=1)
        self.leftframe_title = tk.Label(leftframe, text="Team Members", font=("TKDefaultFont", 14), bg="WHITE", fg="DARK RED")
        self.leftframe_title.grid(row=0, column=0, sticky=tk.W+tk.N, padx=20)
        

    ## ADD A GUY
        self.addguy = tk.Button(leftframe, text="+", relief=tk.FLAT, cursor="hand2", bd=1, bg="WHITE", activebackground="WHITE", font="TKDefaultFont 12", command=self.wizard)
        self.addguy.grid(row=0, column=1, sticky='e', ipadx=4)
        
        
    ## ROSTERBOX
        # self.rosterbox = tk.Listbox(leftframe, activestyle='none', font=("TKDefaultFont 12"))
        self.rosterbox = tree.MultiListbox(leftframe, columns=('Status', 'Name'), font=("TKDefaultFont 12"))
        self.rosterbox_scroll = tk.Scrollbar(leftframe, orient=tk.VERTICAL)
        self.rosterbox['yscrollcommand'] = self.rosterbox_scroll.set
        self.rosterbox_scroll['command'] = self.rosterbox.yview
        self.rosterbox.grid(row=1,column=0, padx=(20,0), columnspan=1, sticky='ns')
        self.rosterbox_scroll.grid(row=1, column=1, rowspan=10, sticky='ns')
        

    ## just some variables we'll be needing
        self.p_first = tk.StringVar()
        self.p_last = tk.StringVar()
        self.p_nickname = tk.StringVar()
        self.p_phone = tk.StringVar()
        self.p_email = tk.StringVar()
        self.p_jvemail = tk.StringVar()
        self.p_jvemail = tk.StringVar()
        self.p_jvemail = tk.StringVar()
        self.p_address = tk.StringVar()
        self.p_city = tk.StringVar()
        self.p_state = tk.StringVar()
        self.p_zip = tk.StringVar()
        self.p_birthday = tk.StringVar()
        self.p_faanum = tk.StringVar()
        self.p_emername = tk.StringVar()
        self.p_emerrel = tk.StringVar()
        self.p_emercell = tk.StringVar()
        self.p_status = tk.StringVar()
        #abilities
        # self.p_weekends = tk.StringVar()
        # self.p_floor = tk.StringVar()
        # self.p_mat = tk.StringVar()
        # self.p_dusk = tk.StringVar()
        # self.p_teaser = tk.StringVar()
        # self.p_premium = tk.StringVar()
        # self.p_luxury = tk.StringVar()
        # self.p_vedit = tk.StringVar()
        # self.p_aes = tk.StringVar()
        # self.p_aev = tk.StringVar()
        # self.p_faa = tk.StringVar()
        # self.p_ains = tk.StringVar()
        # self.p_lins = tk.StringVar()

    
        def viewProfile(event):
            """ Reads profile of the selected photographer """
            target=0
            if self.rosterbox.curselection():
                target = self.rosterbox.curselection()[0]
                print('target =', target)
            
            if target is not None:
                target = self.rosterbox.get(target)[0][1]
                name = target.split(" ")
                self.p_first.set(name[0])
                self.p_last.set(name[1].rstrip('\n'))
                c.execute("SELECT phone, email, jv_email, address, city, state, birthday, faa_num, abilities, emer_name, emer_rel, emer_cell, zip, realtors, notes, nickname, status FROM photographers WHERE first=? AND last=?", (self.p_first.get(), self.p_last.get()))
                info = c.fetchone()
                if info != None:
                    self.p_realtors = info[13]
                    self.p_notes = info[14] 
                    self.p_phone.set(info[0])
                    self.p_email.set(info[1])
                    self.p_jvemail.set(info[2])
                    self.p_address.set(info[3])
                    self.p_city.set(info[4])
                    self.p_state.set(info[5])
                    self.p_birthday.set(info[6])
                    self.p_faanum.set(info[7])
                    self.p_abilities = info[8].lower()
                    # self.p_emername.set(info[9])
                    # self.p_emerrel.set(info[10])
                    # self.p_emercell.set(info[11])
                    self.p_zip.set(info[12])
                    self.p_nickname.set(info[15])
                    self.p_status.set(info[16])
            else:
                target = 0
            updateProfileBox(self)

        #populate the roster box
        c.execute("SELECT first, last, status from Photographers")
        allguys = c.fetchall()
        theRoster = []
        for guy in allguys:
            name = str(guy[0] + ' ' + guy[1])
            if str(guy[2]) == 'None':
                status = '-'
            else:
                print(guy[2])
                status = str(guy[2])
            theRoster.append((status, name))

        for guy in sorted(theRoster):
            self.rosterbox.insert(tk.END, guy[0], guy[1])
            #print(guy[0], guy[1], 'inserted')
               
        self.rosterbox.bind("<Double-Button-1>", viewProfile)  

        #View Profile button that I disabled  
        #tk.Button(leftframe, text="View Profile", font=("TKDefaultFont"), command=lambda:viewProfile(self)).grid(row=6, column=0, ipadx=30, padx=(20,0), sticky='nw')


        def updateProfileBox(self):
            """ updates the photographer profile box """
            self.namelabel.destroy()
            if self.p_nickname.get() == 'None' or self.p_nickname.get() == '':
                self.namelabel = tk.Label(infoFrame, text=(self.p_first.get() + " "  + self.p_last.get()), font=("TKDefaultFont 14"))  
            else:
                self.namelabel = tk.Label(infoFrame, text=(self.p_first.get() + " \'" + self.p_nickname.get() + "\' "  + self.p_last.get()), font=("TKDefaultFont 14"))

            self.namelabel.grid(row=1, column=0, sticky='nw', pady=(6,2), padx=10)
            
            # black horiz line
            tk.Frame(topFrame,height=1, width=215,bg="black").place(x=10, y=32)
            
            self.phonelabel.destroy()

            if self.p_phone.get() != '':
                self.phonelabel = tk.Label(infoFrame, text=self.p_phone.get(), font=("TKDefaultFont 12"))
            else:
                self.phonelabel = tk.Label(infoFrame, text='No phone')
            self.phonelabel.grid(row=3, column=0, sticky='nw', padx=6, pady=(10,0))
            
            self.emaillabel.destroy()
            if self.p_email.get() != '':
                self.emaillabel = tk.Label(infoFrame, text=self.p_email.get(), font=("TKDefaultFont 12"))
            else:
                self.emaillabel = tk.Label(infoFrame, text='No personal email')
            self.emaillabel.grid(row=4, column=0, sticky='nw', padx=6)
            
            self.jvemaillabel.destroy()
            if self.p_jvemail.get() != '':
                self.jvemaillabel = tk.Label(infoFrame, text=self.p_jvemail.get(), font=("TKDefaultFont 12"))
            else:
                self.jvemaillabel = tk.Label(infoFrame, text='No JV email')
            self.jvemaillabel.grid(row=5, column=0, sticky='nw', padx=6)
            
            self.addresslabel.destroy()
            if self.p_address.get() != '':
                self.addresslabel = tk.Label(infoFrame, text=self.p_address.get(), font=("TKDefaultFont 12"))
            else:
                self.addresslabel = tk.Label(infoFrame, text='No address')
            self.addresslabel.grid(row=6, column=0, sticky='nw', padx=6, pady=(6,0))
            
            self.citylabel.destroy()
            self.citylabel = tk.Label(infoFrame, text=self.p_city.get() +", " + self.p_state.get() + " " + self.p_zip.get(), font=("TKDefaultFont 12"))
            self.citylabel.grid(row=7, column=0, sticky='nw', padx=6)
            
            self.birthdaylabel.destroy()
            self.birthdaylabel = tk.Label(infoFrame, text="B-Day: " + self.p_birthday.get(), font=("TKDefaultFont 12"))
            self.birthdaylabel.grid(row=8, column=0, sticky='nw', padx=6, pady=(6,0))
            
            self.faa_numlabel.destroy()
            self.faa_numlabel = tk.Label(infoFrame, text=('FAA#: ' +self.p_faanum.get()), font=("TKDefaultFont 12"))
            self.faa_numlabel.grid(row=9, column=0, sticky='nw', padx=6)
            self.serviceList.delete(0, tk.END)

             
            self.notesList.destroy()
            self.notesList = tk.Text(topFrame, wrap=tk.WORD, height=4, width=45)
            self.notesList.tag_configure('tag-right', font='TKDefaultFont 12', rmargin=3, justify='left')
            
            if self.p_notes != None:
                self.notesList.insert('end', self.p_notes, 'tag-right')
            self.notesList.config(state=tk.DISABLED)
            self.notesList.grid(row=3, column=1, pady=(0,10), padx=(30,0), sticky='nesw')

            self.notesList_scroll.destroy()
            self.notesList_scroll = tk.Scrollbar(topFrame, orient=tk.VERTICAL)
            self.notesList['yscrollcommand'] = self.notesList_scroll.set
            self.notesList_scroll['command'] = self.notesList.yview

            self.notesList_scroll.grid(row=3, column=2, padx=(0, 10), pady=(0,5), sticky='nsw')

            self.realtorList.destroy()
            self.realtorList = tk.Text(services, height=8, width=28)
            self.realtorList.tag_configure('tag-right', font='TKDefaultFont 12', rmargin=3, justify='right')
            
            if self.p_realtors != None:
                self.realtorList.insert('end', self.p_realtors, 'tag-right')
            self.realtorList.config(state=tk.DISABLED)
            self.realtorList.grid(row=1, column=2, sticky='nsew')  

            self.realtorList_scroll.destroy()
            self.realtorList_scroll = tk.Scrollbar(services, orient=tk.VERTICAL)
            self.realtorList['yscrollcommand'] = self.realtorList_scroll.set
            self.realtorList_scroll['command'] = self.realtorList.yview

            self.realtorList_scroll.grid(row=1, column=3, padx=(0,8),sticky='nsw') 

            self.statuslabel.destroy()
            self.statuslabel = tk.Label(infoFrame, text=self.p_status.get(), font = ("TKDefaultFont", 10, "italic"))
            self.statuslabel.grid(row=1, column=1, padx=(0,10), sticky='e')
                
            ab_check(self.p_abilities)
            
    
    ## POPUP COVERAGE   
        def cov_popup(first, last):
            """ Coverage popup window """
            window = tk.Toplevel()
            window.title("Coverage for " + first + " " + last)
            window.wm_iconbitmap('graphics/jvdb.ico')
            boxframe = tk.Frame(window)
            boxframe.grid(row=1, column=0, padx=15, ipady=15)
            cov_box = tk.Listbox(boxframe, width=40, height=30, selectmode=tk.EXTENDED)
            cov_box_scroll = tk.Scrollbar(boxframe, orient=tk.VERTICAL)
            cov_box.grid(row=1, column=0, pady=5, sticky='news')
            cov_box_scroll.grid(row=1, column=1, sticky='nws')
            cov_box['yscrollcommand'] = cov_box_scroll.set
            cov_box_scroll['command'] = cov_box.yview
            c.execute("SELECT UScities.state_id, UScities.city, UScities.county_name FROM UScities LEFT JOIN coverage ON UScities.id=coverage.city_id LEFT JOIN photographers ON coverage.employee_id=photographers.employee_id WHERE photographers.first=? AND photographers.last=?", (first, last,))
            cov_results = c.fetchall()
            cov_list=list()
            count = 0
            for result in cov_results:
                gix = (result[0] + " | " + result[2] + " County | " + result[1])
                cov_list.append(gix)
                count += 1
            cov_list.sort()
            
            for item in cov_list:
                item = str(item)
                cov_box.insert(tk.END, item)
            tk.Label(window, text= first + " " + last + " covers " + str(count) + " towns :").grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

            def export_cov():
                """ Export coverage to txt file """
                try:
                    filename = 'cov_' + first + last + '.txt'
                    filename.replace(' ', '')
                    file = open(filename, 'w')
                except IOError:
                    export_fail.place(relx=.46, rely=.99, anchor='s')
                    visLog('Export of coverage file failed! Is this program in a folder you have permission to write to?')
                    logger.error('Export of coverage file failed!')
                else:
                    file.write("Coverage for " + first + ' ' + last + '\n\n')
                    for line in cov_list:
                        file.write(line + "\n")
                    file.close()
                    export_success.place(relx=.46, rely=.99, anchor='s')
                    print('\''+ filename + '\'' + ' has been exported to the same directory as this program')
                    visLog('\''+ filename + '\'' + ' has been exported to the same directory as this program')
                    logger.info('\''+ filename + '\'' + ' has been exported to the same directory as this program')

            export_button = ttk.Button(boxframe, text = "Export Coverage", command=export_cov)
            export_success = tk.Label(boxframe, text="Export successful", fg='GREEN')
            export_fail = tk.Label(boxframe, text="    Export failed! See log.txt file   ", fg='RED')
            export_button.grid(row=2, column=0, pady=(6,0), ipadx=10)
     
     ## POPUP EMERGENCY   
        def emer_popup(first, last):
            """ Emergency contact pop up window """
            window = tk.Toplevel()
            window.title("Emergency Contact Info for " + first + " " + last)
            window.wm_iconbitmap('graphics/jvdb.ico')
            c.execute("SELECT emer_name, emer_rel, emer_cell FROM Photographers WHERE first=? AND last=?", (first, last))
            emer_results = c.fetchone()
            if emer_results is not None:
                name = str(emer_results[0])
                relation = str(emer_results[1])
                phone = str(emer_results[2])
            else:
                name = ''
                relation = ''
                phone = ''
            boxframe = tk.Frame(window)
            boxframe.grid(row=1, column=0, padx=15, pady=15)
            tk.Label(boxframe, font=("TKDefaultFont", 14), text=("Emergency Contact for " + first + " " + last)).grid(row=0, pady=(0,15))
            tk.Label(boxframe, text=("Name:  " + name)).grid(row=1, sticky='w')
            tk.Label(boxframe, text=("Relation:   " + relation)).grid(row=2, sticky='w')
            tk.Label(boxframe, text=("Phone:   " + phone)).grid(row=3, sticky='w')

    ## POPUP EDIT
        def editPop(self, first, last):
            """ Edit Photographer Info pop up window """
            c.execute("SELECT first, last, nickname, phone, email, jv_email, address, city, state, zip, birthday, faa_num, abilities, realtors, notes, emer_name, emer_rel, emer_cell, status from Photographers where first=? and last=?",(first, last))
            ##################  0      1      2        3     4       5        6         7     8     9      10        11        12       13       14       15          16         17      18
            gix = c.fetchone()
            i = []
            if i != None:
                for record in gix:
                    if record != None:
                        i.append(str(record))
                    else:
                        i.append('')
            editWindow = tk.Toplevel()
            editWindow.title("Edit info for " + first + " " + last)
            editWindow.wm_iconbitmap('graphics/jvdb.ico')
            tk.Label(editWindow, text="Edit Info for " + first + " " + last, font="TKDefaultFont 14").grid(padx=(30,0), pady=10, sticky='nw', columnspan=5)

            info = tk.Frame(editWindow)
            info.grid(row=2, column=0, rowspan=3, sticky=tk.W, padx=30)
            tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
            tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W)
            tk.Label(info, text="Status").grid(row=2, column=0, sticky=tk.W)
            tk.Label(info, text="Phone Number").grid(row=2, column=1, sticky=tk.W)
            tk.Label(info, text="Address").grid(row=4, column=0, sticky=tk.W)
            tk.Label(info, text="City of Residence").grid(row=6, column=0, sticky=tk.W)
            tk.Label(info, text="State").grid(row=4, column=1, sticky=tk.W,)
            tk.Label(info, text="Zip").grid(row=6,column=1, sticky=tk.W)
            tk.Label(info, text="Email").grid(row=8, column=0, sticky=tk.W,)
            tk.Label(info, text="JumpVisual Email").grid(row=10, column=0, sticky=tk.W)
            tk.Label(info, text="Birthday (MM/DD)").grid(row=12, column=0, sticky=tk.W)
            tk.Label(info, text="FAA Certification #").grid(row=12, column=1, sticky=tk.W)
            
            
            self.f = tk.StringVar()
            self.f.set(i[0])
            self.fname_entry = tk.Entry(info, textvariable=self.f)
            self.fname_entry.grid(row=1, column=0, sticky='nw', padx=(0, 20), pady=(0,10))
            
            self.l = tk.StringVar()
            self.l.set(i[1])
            self.lname_entry = tk.Entry(info, textvariable=self.l)
            self.lname_entry.grid(row=1, column=1, sticky=tk.W, pady=(0,10))

            self.status = tk.StringVar()
            self.status.set(i[18])
            self.status_entry = tk.Entry(info, textvariable=self.status)
            self.status_entry.grid(row=3, column=0, sticky=tk.W, pady=(0,10))

            self.phone = tk.StringVar()
            self.phone.set(i[3])
            self.phone_entry = tk.Entry(info, textvariable=self.phone)
            self.phone_entry.grid(row=3, column=1, sticky=tk.W, pady=(0,10))

            self.email = tk.StringVar()
            self.email.set(i[4])
            self.email_entry = tk.Entry(info, textvariable=self.email, width=43)
            self.email_entry.grid(row=9, column=0, sticky=tk.W, columnspan=2, pady=(0,10))
            
            self.jvemail = tk.StringVar()
            self.jvemail.set(i[5])
            self.jvemail_entry = tk.Entry(info, textvariable=self.jvemail, width=43)
            self.jvemail_entry.grid(row=11, column=0, sticky=tk.W, columnspan=2, pady=(0,10))
            
            self.address = tk.StringVar()
            self.address.set(i[6])
            self.address_entry = tk.Entry(info, textvariable=self.address)
            self.address_entry.grid(row=5, column=0, sticky=tk.W, pady=(0,10))
            
            self.city = tk.StringVar()
            self.city.set(i[7])
            self.city_entry = tk.Entry(info, textvariable=self.city)
            self.city_entry.grid(row=7, column=0, sticky=tk.W, pady=(0,10))
            
            self.state = tk.StringVar()
            self.choices=[ 'NJ', 'NY', 'CT', 'PA' ]
            self.statevar = tk.StringVar()
            self.statepulldown = ttk.OptionMenu(info, self.statevar, self.choices[1], *self.choices)
            self.statepulldown.grid(row=5, column=1, sticky=tk.W, pady=(0,10))
            self.statevar.set(i[8])
            
            self.zip = tk.StringVar()
            self.zip.set(i[9])
            self.zip_entry = tk.Entry(info, width=8, textvariable=self.zip)
            self.zip_entry.grid(row=7, column=1, sticky=tk.W, pady=(0,10))
            
            self.birthday = tk.StringVar()
            self.birthday.set(i[10])
            self.birthday_entry = tk.Entry(info, textvariable=self.birthday)
            self.birthday_entry.grid(row=13, column=0, sticky=tk.W, pady=(0,10))
            
            self.faa_num = tk.StringVar()
            self.faa_num.set(i[11])
            self.faa_num_entry = tk.Entry(info, textvariable=self.faa_num)
            self.faa_num_entry.grid(row=13, column=1, sticky=tk.W, pady=(0,10))

            emergency = tk.LabelFrame(info)
            emergency.grid(row=14, column = 0, sticky='nsw', pady=(10,10), ipady=5, columnspan=3, rowspan=4)
            tk.Label(emergency, text="Emergency Contact").grid(row=0, column=0, sticky='w', padx=5, pady=(0,10))
            tk.Label(emergency, text="Name").grid(row=1, column=0, sticky='w', padx=5,)
            tk.Label(emergency, text="Relation").grid(row=1, column=1, sticky='w', padx=5,)
            tk.Label(emergency, text="Phone Number").grid(row=3, column=0, sticky='w', padx=5,)
            
            self.emer_name = tk.StringVar()
            self.emer_name.set(i[15])
            self.emer_name_entry = tk.Entry(emergency, textvariable=self.emer_name)
            self.emer_name_entry.grid(row=2, column=0, sticky=tk.W, padx=(5, 20))
            
            self.emer_relation = tk.StringVar()
            self.emer_relation.set(i[16])
            self.emer_relation_entry = tk.Entry(emergency, width=17, textvariable=self.emer_relation)
            self.emer_relation_entry.grid(row=2, column=1, sticky=tk.W, padx=(5,20))
            
            self.emer_cell = tk.StringVar()
            self.emer_cell.set(i[17])
            self.emer_cell_entry = tk.Entry(emergency, textvariable=self.emer_cell)
            self.emer_cell_entry.grid(row=4, column=0, sticky=tk.W, padx=(5,20))         
            
            tk.Label(info, text="Services").grid(row=0, column=2, sticky='nw', padx=(50,0))
            services = tk.LabelFrame(info, pady=2)
            services.grid(row=1, column=2, rowspan=25, sticky='nw', padx=(50,0))
            self.weekendsvar = tk.IntVar()
            if "WkEnds/" in i[12]:
                self.weekendsvar.set(1)
            tk.Checkbutton(services, text='Work Weekends', variable=self.weekendsvar).grid(row=1, column=0, sticky=tk.W)
            self.floorvar = tk.IntVar()
            if "FP/" in i[12]:
                self.floorvar.set(1)
            tk.Checkbutton(services, text='Floorplans', variable=self.floorvar).grid(row=2, column=0,sticky=tk.W)
            self.duvar = tk.IntVar()
            if "Pdusk/" in i[12]:
                self.duvar.set(1)
            tk.Checkbutton(services, text='Dusk Photography', variable=self.duvar).grid(row=3, column=0, padx=(0,5), sticky=tk.W)
            self.aesvar = tk.IntVar()
            if "Paerial/" in i[12]:
                self.aesvar.set(1)
            tk.Checkbutton(services, text='Aerial stills', variable=self.aesvar).grid(row=4, column=0,sticky=tk.W)
            self.faavar = tk.IntVar()
            if "FAA/" in i[12]:
                self.faavar.set(1)
            tk.Checkbutton(services, text='FAA Certified', variable=self.faavar).grid(row=5, column=0,sticky=tk.W)
            self.a_insvar = tk.IntVar()
            if "InsAerial/" in i[12]:
                self.a_insvar.set(1)
            tk.Checkbutton(services, text='Aerial Insurance', variable=self.a_insvar).grid(row=6, column=0,sticky=tk.W)
            self.l_insvar = tk.IntVar()
            if "InsLiability/" in i[12]:
                self.l_insvar.set(1)
            tk.Checkbutton(services, text='Liability Insurance', variable=self.l_insvar).grid(row=7, column=0,sticky=tk.W)
            
            #tk.Label(services, text="VIDEO SERVICES").grid(row=8, column=0, sticky='ew', pady=(20, 5))
            videoframe = tk.Frame(services, borderwidth=0, relief=tk.GROOVE)
            videoframe.grid(row=0, column=1, sticky=tk.W, rowspan=7)
            self.matvar = tk.IntVar()
            if "Vmatter/" in i[12]:
                self.matvar.set(1)
            tk.Checkbutton(videoframe, text='Matterport', variable=self.matvar).grid(row=0, column=0,sticky=tk.W)
            self.teaservar = tk.IntVar()
            if "Vteaser/" in i[12]:
                self.teaservar.set(1)
            tk.Checkbutton(videoframe, text="Teaser Video", variable=self.teaservar).grid(row=1, column=0,  sticky=tk.W)
            self.premvar = tk.IntVar()
            if "Vpremium/" in i[12]:
                self.premvar.set(1)
            tk.Checkbutton(videoframe, text="Premium Video", variable=self.premvar).grid(row=2, column=0,  sticky=tk.W)
            self.luxvar = tk.IntVar()
            if "Vluxury/" in i[12]:
                self.luxvar.set(1)
            tk.Checkbutton(videoframe, text="Luxury Video", variable=self.luxvar).grid(row=3, column=0, sticky=tk.W)
            self.aevvar = tk.IntVar()
            if "Vaerial/" in i[12]:
                self.aevvar.set(1)
            tk.Checkbutton(videoframe, text='Aerial video', variable=self.aevvar).grid(row=4, column=0, sticky=tk.W)
            self.veditvar = tk.IntVar()
            if "Vediting/" in i[12]:
                self.veditvar.set(1)
            tk.Checkbutton(videoframe, text="Video Editing", variable=self.veditvar).grid(row=5, column=0, sticky=tk.W)
            
            self.newabilities = ''

            notesFrame = tk.Frame(info)
            notesFrame.grid(row=8,column=2, sticky='nsw', columnspan=2, rowspan=10, padx=(50,0), pady=(10, 50))
            tk.Label(notesFrame, text="Notes").grid(row=0, column=0, sticky='nw')

            self.notes = tk.StringVar()
            self.notes.set(i[14])
            self.notes_entry = tk.Text(notesFrame, font=('TKDefaultFont 10'), width=33, height=5)
            self.notes_entry.insert("0.0", i[14])
            self.notes_entry.grid(row=1,  columnspan=3, sticky='nw', pady=(0, 10))
            notes_scroll = tk.Scrollbar(notesFrame, orient=tk.VERTICAL)
            self.notes_entry['yscrollcommand'] = notes_scroll.set
            notes_scroll['command'] = self.notes_entry.yview
            notes_scroll.grid(row=1, column=3, padx=(0, 5), sticky='nsw')

            tk.Label(notesFrame, text="Associated Realtors").grid(row=5, column=0, sticky='sw')
            self.realtors = tk.StringVar()
            self.realtors.set(i[13])
            self.realtors_entry = tk.Text(notesFrame, font=('TKDefaultFont 10'), width=33, height=8)
            self.realtors_entry.insert("0.0", i[13])
            self.realtors_entry.grid(row=6, columnspan=3, sticky='sw')
            realtors_scroll = tk.Scrollbar(notesFrame, orient=tk.VERTICAL)
            self.realtors_entry['yscrollcommand'] = realtors_scroll.set
            realtors_scroll['command'] = self.realtors_entry.yview
            realtors_scroll.grid(row=6, column=3, padx=(0, 5), sticky='nsw')

            ### USER BOX
            column4 = tk.Frame(editWindow)
            column4.grid(row=1, column=4, sticky='nsw', padx=(5,20), rowspan=25)
            tk.Label(column4, text="Current Coverage").grid(row=7, column=0, sticky='w')
            self.userlistbox = tk.Listbox(column4, height=28, width=40, selectmode=tk.EXTENDED)
            self.userlistbox_scroll = tk.Scrollbar(column4, orient=tk.VERTICAL)
            self.userlistbox['yscrollcommand'] = self.userlistbox_scroll.set
            self.userlistbox_scroll['command'] = self.userlistbox.yview
            self.userlistbox.grid(row=8, column=0, rowspan=4, sticky=tk.W)
            self.userlistbox_scroll.grid(row=8, column=1, rowspan=4, sticky='nsw')

            c.execute("SELECT UScities.state_id, UScities.city, UScities.county_name FROM UScities LEFT JOIN coverage ON UScities.id=coverage.city_id LEFT JOIN photographers ON coverage.employee_id=photographers.employee_id WHERE photographers.first=? AND photographers.last=?", (first, last,))
            cov_results = c.fetchall()
            cov_list=list()
            count = 0
            for result in cov_results:
                gix = (result[0] + " | " + result[1] + ", " + result[2] + " County")
                #print("gix is " + gix)
                cov_list.append(gix)
                count += 1
            cov_list.sort()
            #print(cov_list)
            for item in cov_list:
                item = str(item)
                self.userlistbox.insert(tk.END, item)

            ### ALL TOWNS BOX
            column6 = tk.Frame(editWindow)
            column6.grid(row=1, column=6, sticky='nsw', padx=(0,50), rowspan=25)
            tk.Label(column6, text="All Other Towns").grid(row=7, column=0, sticky='w')
            self.alltownbox = tk.Listbox(column6, height=28, width=40, selectmode=tk.EXTENDED)
            self.alltownbox_scroll = tk.Scrollbar(column6, orient=tk.VERTICAL)
            self.alltownbox['yscrollcommand'] = self.alltownbox_scroll.set
            self.alltownbox_scroll['command'] = self.alltownbox.yview
            self.alltownbox.grid(row=8, column=0, rowspan=4, sticky=tk.W)
            self.alltownbox_scroll.grid(row=8, column=1, rowspan=4, sticky='nsw')

            c.execute("SELECT UScities.state_id, UScities.city, UScities.county_name FROM UScities")
            cov_results = c.fetchall()
            cov_list=list()
            count = 0
            for result in cov_results:
                gix = (result[0] + " | " + result[1] + ", " + result[2] + " County")
                #print("gix is " + gix)
                cov_list.append(gix)
                count += 1
            cov_list.sort()
            #print(cov_list)
            for item in cov_list:
                item = str(item)
                self.alltownbox.insert(tk.END, item)


            def confirm_removeGuy(self, first, last):
                """ Delete photographer from database """
                confirm = tk.Toplevel(padx=20, pady=15)
                confirm.wm_iconbitmap('graphics/jvdb.ico')
                center(confirm)
                confirm.title("Are you sure?")
                tk.Label(confirm, text="Are you sure you want to remove " + first + " " + last + "?\nThis cannot be undone!").grid(row=0, columnspan=2, column=0, pady=(0,15), sticky='ew')

                def removeGuy(self, first, last):
                    c.execute("SELECT employee_id FROM photographers WHERE first=? AND last=?", (first, last))
                    targetid = str(c.fetchone()[0])
                    #print("targetid is " + targetid)
                    if targetid != None:
                        c.execute("DELETE FROM coverage WHERE employee_id=?", [targetid])
                        c.execute("DELETE FROM photographers WHERE employee_id=?", [targetid])
                        conn.commit()
                        print(first + " " + last + "'s profile and coverage has been deleted")
                        logger.info(first + " " + last + "'s profile and coverage deleted from database.")
                        confirm.destroy()
                        try:
                            editWindow.destroy()
                        except:
                            pass
                    self.rosterbox.delete(tk.ACTIVE)
                    self.rosterbox.grid(row=1,column=0, padx=(20,0), rowspan=5, columnspan=2, sticky=tk.W+tk.N)
                
                tk.Button(confirm, text="Cancel", command=confirm.destroy).grid(row=1, column=1, ipadx=5, padx=(0, 50), sticky='w')
                tk.Button(confirm, text="Yes", command=lambda:removeGuy(self, first, last)).grid(row=1, column=0, ipadx=10, padx=(60, 0))

            def makeChanges(self):
                """ Write changes to photographer's profile """
                nameChanged = False
                statusChanged = False
                if self.weekendsvar.get() == 1:
                    self.newabilities += "WkEnds/"
                    ##print("Video added to abilities")
                if self.floorvar.get() == 1:
                    self.newabilities += "FP/"
                    ##print("Floorplans added to abilities")
                if self.duvar.get() == 1:
                    self.newabilities += "Pdusk/"
                    ##print("Dusk photography added to abilities")
                if self.aesvar.get() == 1:
                    self.newabilities += "Paerial/"
                    ##print("Aerial Stills added to abilities")
                if self.faavar.get() == 1:
                    self.newabilities += "FAA/"
                    ##print("FAA Certification added to abilities")
                if self.matvar.get() == 1:
                    self.newabilities += "Vmatter/"
                    ##print("Matterport added to abilities")
                if self.teaservar.get() == 1:
                    self.newabilities += "Vteaser/"
                    ##print("Teaser video added to abilities")
                if self.premvar.get() == 1:
                    self.newabilities += "Vpremium/"
                    ##print("Premium Video added to abilities")
                if self.luxvar.get() == 1:
                    self.newabilities += "Vluxury/"
                    ##print("Luxury Video added to abilities")
                if self.aevvar.get() == 1:
                    self.newabilities += "Vaerial/"
                    ##print("Aerial Video added to abilities")
                if self.veditvar.get() == 1:
                    self.newabilities += "Vediting/"
                if self.a_insvar.get() == 1:
                    self.newabilities += "InsAerial/"
                if self.l_insvar.get() == 1:
                    self.newabilities += "InsLiability/"
                if self.fname_entry.get() != first or self.lname_entry.get() != last:
                    nameChanged = True
                if self.status_entry.get() != status:
                    statusChanged = True
                c.execute('UPDATE photographers SET first=?, last=?, status=?, phone=?, email=?, jv_email=?, address=?, city=?, state=?, zip=?, birthday=?, faa_num=?, realtors=?, notes=?, emer_name=?, emer_rel=?, emer_cell=?, abilities=? where first=? AND last=?',(self.fname_entry.get().rstrip().replace(' ', '_'), self.lname_entry.get().rstrip().replace(' ', '_'), self.status_entry.get(), self.phone_entry.get(), self.email_entry.get(), self.jvemail_entry.get(), self.address_entry.get(), self.city_entry.get(), self.statevar.get(), self.zip_entry.get(), self.birthday_entry.get(), self.faa_num_entry.get(), self.realtors_entry.get('1.0', tk.END), self.notes_entry.get('1.0', tk.END), self.emer_name_entry.get(), self.emer_relation_entry.get(), self.emer_cell_entry.get(), self.newabilities, first, last))
                # Wipe out all photographer's coverage...will be rewritten
                c.execute('SELECT employee_id from photographers where first=? and last=?', (first, last))
                tar_id = str(c.fetchone()[0])
                c.execute('DELETE from Coverage WHERE employee_id =?',(tar_id,))
                usertowns = self.userlistbox.get(0, tk.END)
                # Rewriting photographer's coverage
                for town in usertowns:
                    # print(town)
                    town = town.replace(' County','')
                    gix = town.split(' | ')
                    bix = gix[1].split(', ')
                    tarstate = gix[0]
                    tartown = bix[0]
                    tarcounty = bix[1]
                    c.execute('SELECT id from UScities where state_id=? and county_name=? and city=?',(tarstate, tarcounty, tartown))
                    tar_cityid = str(c.fetchone()[0])
                    c.execute('INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)', (tar_id, tar_cityid))

                conn.commit()
                print("Edits made to " + self.fname_entry.get() + " " + self.lname_entry.get())
                logger.info("Edits made to " + self.fname_entry.get() + " " + self.lname_entry.get())

                if nameChanged or statusChanged: #if there's been a change made to the name, update the name in the roster list
                    index = self.rosterbox.index(tk.ACTIVE)
                    self.rosterbox.delete(index)
                    self.rosterbox.insert(index, self.status_entry.get(), self.fname_entry.get() + ' ' + self.lname_entry.get())
                    self.rosterbox.grid(row=1,column=0, padx=(20,0), columnspan=1, sticky='ns')
                editWindow.destroy()
            
            ttk.Button(editWindow, text="Delete Photographer", command=lambda:confirm_removeGuy(self, first, last)).grid(row=5, column=6, padx=(0,30), pady=(10, 15), ipadx=8, sticky='ne')
            ttk.Button(editWindow, text="Save Changes",  command=lambda:makeChanges(self)).grid(row=5, column=0, padx=(30,0), pady=(10, 15), ipadx=8, sticky='nw')

            def add_town():
                """ Add town to photographer's coverage list """
                if len(self.alltownbox.curselection()) > 1:
                    for val in self.alltownbox.curselection():
                        self.userlistbox.insert(tk.END, self.alltownbox.get(val))
                    for i in range(len(self.alltownbox.curselection())):
                        self.alltownbox.delete(self.alltownbox.curselection()[0])
                else:
                    self.userlistbox.insert(tk.END, self.alltownbox.get(tk.ACTIVE))
                    self.alltownbox.delete(tk.ACTIVE)
            
                
            def del_town():
                """ Delete town from photographer's coverage list """
                if len(self.userlistbox.curselection()) > 1:
                    for i in range(len(self.userlistbox.curselection())):
                        self.userlistbox.delete(self.userlistbox.curselection()[0])
                else:
                    self.alltownbox.insert(tk.END, self.userlistbox.get(tk.ACTIVE))
                    self.userlistbox.delete(tk.ACTIVE)

            ### TRANSFER BUTTONS
            column5 = tk.Frame(editWindow)
            column5.grid(row=1, column=5, sticky='nsw', padx=(0,20), rowspan=25)
            ttk.Button(column5, text="<<  Add", width=12, command=lambda:add_town()).grid(row=0, column=5, padx=0, pady=(200,15))
            ttk.Button(column5, text="Remove  >>",  width=12, command=lambda:del_town()).grid(row=1, column=5,padx=0)

            root.wait_window(editWindow)
            viewProfile(self)

    ## TOP FRAME
        topFrame = tk.Frame(self, bd=2, width=500, relief=tk.RAISED)
        topFrame.columnconfigure(0, weight=1)
        topFrame.columnconfigure(1, weight=3)
        topFrame.rowconfigure(0, weight=1)
        topFrame.rowconfigure(3, weight=1)
        topFrame.grid(row=1, column=1, sticky='news', rowspan=2, padx=15, pady=(0,5), ipadx=2)
        infoFrame = tk.Frame(topFrame, width=300)
        infoFrame.grid(row=0, column=0, rowspan=4, sticky='news')
        infoFrame.columnconfigure(0, minsize=320, weight=1)
        infoFrame.rowconfigure(9, weight=1)

        self.statuslabel = tk.Label(infoFrame, text=self.p_status.get(), font = ("TKDefaultFont 10"))
        self.namelabel = tk.Label(infoFrame, text=(self.p_first.get() + " " + self.p_last.get()), font=("TKDefaultFont", 14))
        self.namelabel.grid(row=1,  sticky=tk.W, pady=2, padx=6)
        self.addresslabel = tk.Label(infoFrame, text=self.p_address.get())
        self.addresslabel.grid(row=4, sticky=tk.W, pady=2, padx=6)
        self.phonelabel = tk.Label(infoFrame, text=self.p_phone.get())
        self.phonelabel.grid(row=5, sticky=tk.W, pady=2, padx=6)
        self.emaillabel = tk.Label(infoFrame, text=self.p_email.get())
        self.emaillabel.grid(row=6,  sticky=tk.W, pady=2, padx=6)
        self.jvemaillabel = tk.Label(infoFrame, text=self.p_jvemail.get())
        self.jvemaillabel.grid(row=7, sticky=tk.W, pady=2, padx=6)
        self.birthdaylabel = tk.Label(infoFrame, text=self.p_birthday.get())
        self.birthdaylabel.grid(row=8, sticky=tk.W, pady=2, padx=6)
        self.faa_numlabel = tk.Label(infoFrame, text=("FAA#: " +self.p_faanum.get()))
        self.faa_numlabel.grid(row=9, sticky=tk.W, pady=2, padx=6)
        buttons = tk.Frame(infoFrame)
        buttons.grid(row=9, column=0, sticky='sew', rowspan=2, columnspan=2, pady=(20, 5), padx=6)
        buttons.columnconfigure(1, weight=1)

        ttk.Button(buttons, text="Coverage",  width="15", command=lambda:cov_popup(self.p_first.get(), self.p_last.get())).grid(row=0, column=0, sticky='ws', ipadx=2, padx=(0,5), pady=(20,0))
        ttk.Button(buttons, text="Emergency",  width="15", command=lambda:emer_popup(self.p_first.get(), self.p_last.get())).grid(row=1, column=0, sticky='ws', ipadx=2, padx=(0,5), pady=(5,0))
        ttk.Button(buttons, text="Business Card", width="15", command=lambda:emer_popup(self.p_first.get(), self.p_last.get())).grid(row=2, column=0, sticky='ws', ipadx=2, padx=(0,5), pady=(5,0))
        ttk.Button(buttons, text="Edit", command=lambda:editPop(self, self.p_first.get(), self.p_last.get())).grid(row=2,column=1, sticky='es', ipadx=5)
        
        self.citylabel = tk.Label(infoFrame, text=self.p_city.get() +", " + self.p_state.get() + " " + self.p_zip.get())

        #services list
        services = tk.Frame(topFrame)
        #services.columnconfigure(2, weight=1)
        services.grid(row=0, column=1, columnspan=2, padx=(30,0), sticky='news')
        services.columnconfigure(0, weight=1)
        services.columnconfigure(2, weight=3)
        services.rowconfigure(1, weight=1)
        tk.Label(services, text="Services", font=("TKDefaultFont 8 bold")).grid(row=0, column=0, pady=(9,0), sticky='w')
        self.serviceList = tk.Listbox(services, activestyle='none', font="TKDefaultFont 12")

        self.serviceList.grid(row=1, column=0, sticky='nsew')

        serviceList_scroll = tk.Scrollbar(services, orient=tk.VERTICAL)
        self.serviceList['yscrollcommand'] = serviceList_scroll.set
        serviceList_scroll['command'] = self.serviceList.yview
        serviceList_scroll.grid(row=1, column=1, padx=(0, 5), sticky='nsw')
        
        # notes
        tk.Label(topFrame, text="Notes", font=("TKDefaultFont 8 bold")).grid(row=2, column=1, sticky='ne')
        self.notesList = tk.Text(topFrame, height=5, width=25)
        # self.notesList.grid(row=4, column=0, sticky='w')
        self.notesList_scroll = tk.Scrollbar(topFrame, orient=tk.VERTICAL)
        
        # realtors
        tk.Label(services, text="Associated Realtors", font=("TKDefaultFont 8 bold")).grid(row=0, column=2, pady=(9,0), sticky='e')
        self.realtorList = tk.Text(services, width=45, height=7)
        # self.realtorList.grid(row=1, column=2, sticky='ne')
        self.realtorList_scroll = tk.Scrollbar(services, orient=tk.VERTICAL)

        
        def ab_check(abilities):
            """ reads and decyphers abilities code """
            #print("abilities is " + abilities)
            if "fp" in str(abilities):
                self.serviceList.insert(tk.END, " Floorplans")

            if "wkends" in abilities:
                self.serviceList.insert(tk.END, " Weekends")
                
            if "vmatter" in abilities:
                self.serviceList.insert(tk.END, " Matterport")
                
            if "pdusk" in abilities:
                self.serviceList.insert(tk.END, " Dusk Photos")
                
            if "vteaser" in abilities:
                self.serviceList.insert(tk.END, " Teaser Vid")
                
            if "vpremium" in abilities:
                self.serviceList.insert(tk.END, " Premium Vid")
                
            if "vluxury" in abilities:
                self.serviceList.insert(tk.END, " Luxury Vid")
                
            if "vediting" in abilities:
                self.serviceList.insert(tk.END, " Video Edit")
                
            if "paerial" in abilities:
                self.serviceList.insert(tk.END, " Aerial Stills")
                
            if "vaerial" in abilities:
                self.serviceList.insert(tk.END, " Aerial Video")
                
            if "faa" in abilities:
                self.serviceList.insert(tk.END, " FAA Certified")
                
            if "insaerial" in abilities:
                self.serviceList.insert(tk.END, " Aerial Ins.")
            
            if "insliab" in abilities:
                self.serviceList.insert(tk.END, " Liability Ins.")
            
        
        ab_check(self.p_abilities)
        
        if (self.rosterbox.get(0) == ''):
            self.rosterbox.insert(tk.END, 'Uh-oh', 'Empty!')
        else:
            viewProfile(self)
    
    ## BOTTOM FRAME
        bottomFrame = tk.Frame(self,bd=2, relief=tk.RAISED)
        bottomFrame.grid(row=3, column=0, sticky='news', columnspan=2, pady=10, padx=15, ipadx=10, ipady=10)
        bottomFrame.columnconfigure(4, weight=1)
        bottomFrame.rowconfigure(2, weight=1)
        tk.Label(bottomFrame, text="Search by City", font="TKDefaultFont 12").grid(row=0, column=0, sticky=tk.W, pady=6, padx=(20,6))
        
        state_int = tk.IntVar()
        state_int.set(0)
        tk.Radiobutton(bottomFrame, text="NJ", variable=state_int, value="0", command=lambda:state_int.set(0)).grid(row=1, column=0)
        tk.Radiobutton(bottomFrame, text="NY", variable=state_int, value="1", command=lambda:state_int.set(1)).grid(row=1, column=1)
        tk.Radiobutton(bottomFrame, text="CT", variable=state_int, value="2", command=lambda:state_int.set(2)).grid(row=1, column=2)
        searchBox = tk.Entry(bottomFrame, width=25, font="TKDefaultFont 12")
        searchBox.grid(row=0, column=1, columnspan=3, pady=(15,6), sticky='ew')
        
        
        def duplicateTownPop(results, city, state):
            """ Pops up a window if there are two towns with the same name in that state (eg. Monroe NJ)"""
            count = len(results)
            count = str(count)
            window = tk.Toplevel()
            window.title("Which one?")
            tk.Label(window, text=("There are {num} towns named {townname} in {thatstate}.\nWhich one did you want?".format(num=count, townname=city, thatstate=state))).grid(row=0, column=0, sticky='ew', padx=20, pady=10,)
            duperesultsBox = tk.Listbox(window, height=5, width=45)
            duperesultsBox.grid(row=1, column=0, pady=(0,10), padx=10)
            for result in results:
                choice = result[0] + ', ' + result[1] + ' County' 
                duperesultsBox.insert(tk.END, choice)
                
            def pickTown():
                """ Select the correct desired town """
                picked = duperesultsBox.get(tk.ACTIVE)
                choice = picked.split(', ')
                choice[1] = choice[1].replace(' County', '')
                window.destroy()
                c.execute("SELECT first, last, photographers.city, abilities FROM photographers LEFT JOIN coverage ON photographers.employee_ID=coverage.employee_ID LEFT JOIN USCities on coverage.city_id=UScities.id WHERE UScities.city = ? AND UScities.county_name=? AND UScities.state_id=?", (choice[0], choice[1], state))
                whatigot = c.fetchall()
                if len(whatigot)==0:
                    resultsBox.insert(tk.END, "Sorry, no results. Check your spelling?")
                else:
                    for guy in whatigot:
                        if guy[2] == choice[0]:  
                            resultsBox.insert(tk.END, guy[0] + " " + guy[1] + " lives there." + "  ["+ guy[3]+"]")
                        else:
                            resultsBox.insert(tk.END, guy[0] + " " + guy[1] + "  ["+ guy[3]+"]")
                
            tk.Button(window, text="OK",command=pickTown).grid(row=3, column=0, ipadx=10, pady=10)
                
            
            
        def searchcity(state_int):
            """ search photographer coverage by city """
            if state_int.get()==0:
                searchstate = "NJ"
            elif state_int.get()==1:
                searchstate = "NY"
            else:
                searchstate = "CT"
            resultsBox.delete(0, tk.END)
            query = searchBox.get()
            #print(query + " was searched")
            c.execute("SELECT city, county_name, id FROM USCities WHERE state_id=? AND city=?",(searchstate, query.title()))
            townResults = c.fetchall()
            #print(townResults)
            if len(townResults) > 1: #Pop up a window if there's more than one town by that name in the state
                duplicateTownPop(townResults, query.title(), searchstate)
                
            else:
                c.execute("SELECT first, last, photographers.city, abilities, realtors, notes FROM photographers LEFT JOIN coverage ON photographers.employee_ID=coverage.employee_ID LEFT JOIN USCities on coverage.city_id=UScities.id WHERE UScities.city = ? AND UScities.state_id=?", (query.title(), searchstate))
                whatigot = c.fetchall()

                if len(whatigot)==0:
                    resultsBox.insert(tk.END, "Sorry, no results. Check your spelling?")
                else:
                    
                    result_amt = len(whatigot)
                    for guy in whatigot:
                        result = guy[0] + " " + guy[1]

                        if guy[2] == query.title(): #if photographer lives in the town searched
                            result += " lives there.   "

                        result += ' [' +guy[3]+']' #append abilities

                        # if guy[4] != None: #if realtors isn't blank, append realtors
                        #     realtors = guy[4].rstrip().replace('\n', ' ')
                        #     result += "    R: " + realtors
                        
                        # if guy[5] != None: #if notes aren't blank, append notes
                        #     notes = guy[5].rstrip().replace('\n', ' ')
                        #     result += "   N: " + notes
                        
                        resultsBox.insert(tk.END, result)
                        tk.Label(bottomFrame,text = (str(result_amt) + ' results')).grid(row=1, column=4, padx=(100, 0), sticky='es')
            
        def enterhit(event):
            searchcity(state_int)
        
        searchBox.bind("<Return>", enterhit)
            
        searchbutton = ttk.Button(bottomFrame, text="Search", command=lambda:searchcity(state_int))
        searchbutton.grid(row=0, column=4, padx=6, ipadx=10, sticky='w')
        
        resultsBox = tk.Listbox(bottomFrame, width=50, font="Arial 14", selectmode="EXTENDED")
        resultsBox.grid(row=2, column=0, pady=(5,20), padx=(20, 0), columnspan=5, sticky='news')
        resultsBox_scroll = tk.Scrollbar(bottomFrame, orient=tk.VERTICAL)
        resultsBox['yscrollcommand'] = resultsBox_scroll.set
        resultsBox_scroll['command'] = resultsBox.yview
        resultsBox_scroll.grid(row=2, column=5, padx=(0, 20), sticky='nsw')
        
        resultsBox_scroll2 = tk.Scrollbar(bottomFrame, orient=tk.HORIZONTAL)
        resultsBox['xscrollcommand'] = resultsBox_scroll2.set
        resultsBox_scroll2['command'] = resultsBox.xview
        #resultsBox_scroll2.grid(row=3, column=0, padx=(20,0), pady=(0,20), sticky='news', columnspan=5)
    
    ## LOG FRAME
        """ Maybe for a future version """
        self.logFrame = tk.Frame(self, height=20, bg="WHITE")
        self.logMessage = tk.Label(self.logFrame, bg="WHITE", fg="GRAY", font="TKDefaultFont 14", text="")
        self.logFrame.grid(row=4, column=0, sticky='ew', columnspan=2, pady=5, padx=15, ipadx=5, ipady=4)
        self.logMessage.pack()

        




          
### START PROGRAM
if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()
    app = root()
    app.mainloop()
    sys.exit(0)
    

    
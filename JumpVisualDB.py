import sqlite3
import os
import shutil
import hashlib
import datetime
import tkinter as tk
from tkinter import ttk
import dateformat
import wizardpop
import backerupper
import config
import otherframes
## Created by John Gallino
## December, 2018

#TO DO LIST
# Add editing capability

conn = sqlite3.connect('jump.db')
c = conn.cursor()
files = []
path = "photographers"
version = "version 4.1"

# with conn:
#     c.execute("SELECT id FROM UScities WHERE state_id=? AND county_name=? AND city=?",('NJ', 'Bergen', 'Emerson'))
#     townID = c.fetchone()
#     print('townID is ' + str(townID[0]))

def access():
    print("accessed jumpvisualdb")

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

def clearPhotographers():
    c.execute("DELETE FROM photographers")
    conn.commit()


def wizard():
    '''opens the New Guy wizard screen'''
    config.newuser = ''
    wizard = wizardpop.wizardpop()
    root.wait_window(wizard.window)
    wizard.window.destroy()
    otherframes.i = 0
    rosterbox.insert('end', config.newuser)
    rosterbox.grid(row=1,column=0, padx=(20,0), rowspan=5, columnspan=2, sticky=tk.W+tk.N)
    
def bye():
    quit(1)
    
### ROOT SCREEN
class root(tk.Tk):
    """ JazzSoft root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      ##MAIN WINDOW  
        self.title("JumpVisual Dispatch Protocol " + version)
        self.configure(bg="WHITE")
        #self.geometry("720x575")
        self.resizable(width=False, height=False)
        self.columnconfigure(1, weight=1)
        self.wm_iconbitmap('jvdb.ico')
        #self.overrideredirect(1)
        # self.bind('<Button-1>',self.clickwin)
        # self.bind('<B1-Motion>',self.dragwin)
        self.p_abilities = ''
        self.p_notes = ''
        self.p_realtors = ''
    ## TOP IMAGE
        self.headimg = tk.PhotoImage(file="dispatch.pbm")
        self.banner = tk.Label(self,bg='white', image=self.headimg)
        
        self.banner.image = self.headimg
        self.banner.grid(row=0, column=0, columnspan=10, sticky=tk.W+tk.E)

        #tk.Label(self, text=version, bg="WHITE").grid(row=0, column=1, ipadx=15, sticky='es') #version label
        #tk.Button(self, text="X", fg="DARK RED", font='Verdana 10', relief=tk.FLAT, bg="WHITE", command=bye).grid(row=0, column=1, padx=10, pady=(5,0), sticky='ne')
    ## LEFT FRAME
        leftframe = tk.Frame(self, bg="WHITE")
        leftframe.grid(row=1, column=0, sticky='nw', rowspan=8)
        tk.Label(leftframe, text="Team Members", font=("TKDefaultFont", 14), bg="WHITE", fg="DARK RED").grid(row=0, column=0, sticky=tk.W+tk.N, padx=20)

    ## ADD A GUY
        tk.Button(leftframe, text="+", relief=tk.FLAT, cursor="hand2", bd=1, bg="WHITE", activebackground="WHITE", font="TKDefaultFont 8", command=wizard).grid(row=0, column=1, sticky='e', ipadx=4)
        global rosterbox
        rosterbox = tk.Listbox(leftframe, width=20, height=13, activestyle='none', font=("TKDefaultFont"))
        rosterbox_scroll = tk.Scrollbar(leftframe, orient=tk.VERTICAL)
        rosterbox['yscrollcommand'] = rosterbox_scroll.set
        rosterbox_scroll['command'] = rosterbox.yview
        rosterbox.grid(row=1,column=0, padx=(20,0), rowspan=5, columnspan=2, sticky=tk.W+tk.N)
        rosterbox_scroll.grid(row=1, column=1, rowspan=5, sticky=tk.N+tk.S+tk.E)
        #tk.Label(leftframe, text=version, bg="WHITE", fg="GRAY").grid(row=7, column=0, padx=5, pady=6, sticky='swe')

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
        #abilities
        self.p_weekends = tk.StringVar()
        self.p_floor = tk.StringVar()
        self.p_mat = tk.StringVar()
        self.p_dusk = tk.StringVar()
        self.p_teaser = tk.StringVar()
        self.p_premium = tk.StringVar()
        self.p_luxury = tk.StringVar()
        self.p_vedit = tk.StringVar()
        self.p_aes = tk.StringVar()
        self.p_aev = tk.StringVar()
        self.p_faa = tk.StringVar()
        self.p_ains = tk.StringVar()
        self.p_lins = tk.StringVar()

    
        def viewProfile(event):
            """ Reads profile of the selected photographer """
            target = rosterbox.get(tk.ACTIVE).rstrip('\n')
            name = target.split(" ")
            self.p_first.set(name[0])
            self.p_last.set(name[1].rstrip('\n'))
            #print("p_first is " + self.p_first.get() + "\np_last is " + self.p_last.get())
            c.execute("SELECT phone, email, jv_email, address, city, state, birthday, faa_num, abilities, emer_name, emer_rel, emer_cell, zip, realtors, notes, nickname FROM photographers WHERE first=? AND last=?", (self.p_first.get(), self.p_last.get()))
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
                #print("p_abilities is " + self.p_abilities) 
                self.p_emername.set(info[9])
                self.p_emerrel.set(info[10])
                self.p_emercell.set(info[11])
                self.p_zip.set(info[12])
                self.p_nickname.set(info[15])
                    
            updateProfileBox(self)

        #populate the roster box
        c.execute("SELECT first, last from Photographers")
        allguys = c.fetchall()
        theRoster = []
        for guy in allguys:
            name = str(guy[0] + ' ' + guy[1])
            theRoster.append(name)

        for guy in sorted(theRoster):
            rosterbox.insert(tk.END, guy.title())
               

        rosterbox.bind("<Double-Button-1>", viewProfile)  

        #View Profile button that I disabled  
        #tk.Button(leftframe, text="View Profile", font=("TKDefaultFont"), command=lambda:viewProfile(self)).grid(row=6, column=0, ipadx=30, padx=(20,0), sticky='nw')


        def updateProfileBox(self):
            """ updates the dang ole profile box """
            self.namelabel.destroy()
            #print("p_nickname is " + self.p_nickname.get())
            if self.p_nickname.get() == 'None' or self.p_nickname.get() == '':
                self.namelabel = tk.Label(infoFrame, text=(self.p_first.get() + " "  + self.p_last.get()), font=("TKDefaultFont 14"))  
            else:
                self.namelabel = tk.Label(infoFrame, text=(self.p_first.get() + " \'" + self.p_nickname.get() + "\' "  + self.p_last.get()), font=("TKDefaultFont 14"))

            self.namelabel.grid(row=1, column=0, sticky=tk.W, pady=(6,2), padx=10)
            
            # this is black horiz line
            tk.Frame(topFrame,height=1, width=200 ,bg="black").place(x=10, y=30)
            
            self.phonelabel.destroy()

            if self.p_phone.get() != '':
                self.phonelabel = tk.Label(infoFrame, text=self.p_phone.get())
            else:
                self.phonelabel = tk.Label(infoFrame, text='No phone')
            self.phonelabel.grid(row=3, column=0, sticky='nw', padx=6)
            
            self.emaillabel.destroy()
            if self.p_email.get() != '':
                self.emaillabel = tk.Label(infoFrame, text=self.p_email.get())
            else:
                self.emaillabel = tk.Label(infoFrame, text='No personal email')
            self.emaillabel.grid(row=4, column=0, sticky='nw', padx=6)
            
            self.jvemaillabel.destroy()
            if self.p_jvemail.get() != '':
                self.jvemaillabel = tk.Label(infoFrame, text=self.p_jvemail.get())
            else:
                self.jvemaillabel = tk.Label(infoFrame, text='No JV email')
            self.jvemaillabel.grid(row=5, column=0, sticky='nw', padx=6)
            
            self.addresslabel.destroy()
            if self.p_address.get() != '':
                self.addresslabel = tk.Label(infoFrame, text=self.p_address.get())
            else:
                self.addresslabel = tk.Label(infoFrame, text='No address')
            self.addresslabel.grid(row=6, column=0, sticky='nw', padx=6, pady=(6,0))
            
            self.citylabel.destroy()
            self.citylabel = tk.Label(infoFrame, text=self.p_city.get() +", " + self.p_state.get() + " " + self.p_zip.get())
            self.citylabel.grid(row=7, column=0, sticky='nw', padx=6)
            
            self.birthdaylabel.destroy()
            self.birthdaylabel = tk.Label(infoFrame, text="B-Day: " + self.p_birthday.get())
            self.birthdaylabel.grid(row=8, column=0, sticky='nw', padx=6, pady=(6,0))
            
            self.faa_numlabel.destroy()
            self.faa_numlabel = tk.Label(infoFrame, text=('FAA#: ' +self.p_faanum.get()))
            self.faa_numlabel.grid(row=9, column=0, sticky='nw', padx=6)
            self.serviceList.delete(0, tk.END)

            self.notesList.destroy()
            self.notesList = tk.Text(topFrame, wrap=tk.WORD, height=4, width=45)
            self.notesList.tag_configure('tag-right', font='TKDefaultFont 10', rmargin=3, justify='right')
            
            if self.p_notes != None:
                self.notesList.insert('end', self.p_notes, 'tag-right')
            self.notesList.config(state=tk.DISABLED)
            self.notesList.grid(row=3, column=1, pady=(0,10), sticky='nsw')

            self.notesList_scroll.destroy()
            self.notesList_scroll = tk.Scrollbar(topFrame, orient=tk.VERTICAL)
            self.notesList['yscrollcommand'] = self.notesList_scroll.set
            self.notesList_scroll['command'] = self.notesList.yview

            self.notesList_scroll.grid(row=3, column=2, padx=(0, 10), pady=(0,5), sticky='nsw')

            self.realtorList.destroy()
            self.realtorList = tk.Text(services, height=8, width=28)
            self.realtorList.tag_configure('tag-right', font='TKDefaultFont 10', rmargin=3, justify='right')
            
            if self.p_realtors != None:
                self.realtorList.insert('end', self.p_realtors, 'tag-right')
            self.realtorList.config(state=tk.DISABLED)
            self.realtorList.grid(row=1, column=2, sticky='ne')  

            self.realtorList_scroll.destroy()
            self.realtorList_scroll = tk.Scrollbar(services, orient=tk.VERTICAL)
            self.realtorList['yscrollcommand'] = self.realtorList_scroll.set
            self.realtorList_scroll['command'] = self.realtorList.yview

            self.realtorList_scroll.grid(row=1, column=3, padx=(0,8),sticky='nsw') 
                
            ab_check(self.p_abilities)
            
    
    ## POPUP COVERAGE   
        def cov_popup(first, last):
            window = tk.Toplevel()
            window.title("Coverage for " + first + " " + last)
            window.wm_iconbitmap('jvdb.ico')
            boxframe = tk.Frame(window)
            boxframe.grid(row=1, column=0, padx=15, ipady=15)
            cov_box = tk.Listbox(boxframe, width=40, height=30)
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
                gix = (result[0] + " | " + result[1] + ", " + result[2] + " County")
                #print("gix is " + gix)
                cov_list.append(gix)
                count += 1
            cov_list.sort()
            #print(cov_list)
            for item in cov_list:
                item = str(item)
                cov_box.insert(tk.END, item)
            tk.Label(window, text= first + " " + last + " covers " + str(count) + " towns :").grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

            def export_cov():
                try:
                    filename = 'cov_' + first + last + '.txt'
                    filename.replace(' ', '')

                    file = open(filename, 'w')
                    file.write("Coverage for " + first + ' ' + last + '\n\n')
                    #file.write("DO NOT add towns to this list that did not\n#\tappear in the wizard. Please notify johngallino@gmail.com or\n#\t@gallino on Slack about any missing towns.\n")
                    for line in cov_list:
                        file.write(line + "\n")
                    file.close()
                    export_success.place(relx=.46, rely=.99, anchor='s')
                    print('\''+ filename + '\'' + ' has been exported to the same directory as this program')
                except:
                    export_fail.place(relx=.46, rely=.99, anchor='s')
                    print('Export of coverage file failed. What the hell?')

            export_button = ttk.Button(boxframe, text = "Export Coverage", command=export_cov)
            export_success = tk.Label(boxframe, text="Export successful", fg='GREEN')
            export_fail = tk.Label(boxframe, text="    Export failed!    ", fg='RED')
            export_button.grid(row=2, column=0, pady=(6,0), ipadx=10)
     
     ## POPUP EMERGENCY   
        def emer_popup(first, last):
            window = tk.Toplevel()
            window.title("Emergency Contact Info for " + first + " " + last)
            window.wm_iconbitmap('jvdb.ico')
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

            c.execute("SELECT first, last, nickname, phone, email, jv_email, address, city, state, zip, birthday, faa_num, abilities, realtors, notes, emer_name, emer_rel, emer_cell from Photographers where first=? and last=?",(first, last))
            ##################  0      1      2        3     4       5        6         7     8     9      10        11        12       13       14       15          16         17
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
            editWindow.wm_iconbitmap('jvdb.ico')
            tk.Label(editWindow, text="Edit Info for " + first + " " + last, font="TKDefaultFont 14").grid(padx=(30,0), pady=10, sticky='nw', columnspan=5)

            info = tk.Frame(editWindow)
            info.grid(row=2, column=0, rowspan=3, sticky=tk.W, padx=30)
            tk.Label(info, text="First Name").grid(row=0, column=0, sticky=tk.W)
            tk.Label(info, text="Last Name").grid(row=0, column=1, sticky=tk.W)
            tk.Label(info, text="Nickname").grid(row=2, column=0, sticky=tk.W)
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

            self.nick = tk.StringVar()
            self.nick.set(i[2])
            self.nick_entry = tk.Entry(info, textvariable=self.nick)
            self.nick_entry.grid(row=3, column=0, sticky=tk.W, pady=(0,10))

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
            self.userlistbox = tk.Listbox(column4, height=28, width=40)
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
            self.alltownbox = tk.Listbox(column6, height=28, width=40)
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
                confirm = tk.Toplevel(padx=15, pady=15)
                confirm.wm_iconbitmap('jvdb.ico')
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
                        confirm.destroy()
                        try:
                            editWindow.destroy()
                        except:
                            print("weird error but everything is okay. just close the Edit window")
                    rosterbox.delete(tk.ACTIVE)
                    rosterbox.grid(row=1,column=0, padx=(20,0), rowspan=5, columnspan=2, sticky=tk.W+tk.N)
                
                tk.Button(confirm, text="Cancel", command=confirm.destroy).grid(row=1, column=1, ipadx=5, padx=(0, 50), sticky='w')
                tk.Button(confirm, text="Yes", command=lambda:removeGuy(self, first, last)).grid(row=1, column=0, ipadx=10, padx=(50, 10))
        

            def makeChanges(self):
                flag = False
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
                    flag = True
                c.execute('UPDATE photographers SET first=?, last=?, nickname=?, phone=?, email=?, jv_email=?, address=?, city=?, state=?, zip=?, birthday=?, faa_num=?, realtors=?, notes=?, emer_name=?, emer_rel=?, emer_cell=?, abilities=? where first=? AND last=?''',(self.fname_entry.get(), self.lname_entry.get(), self.nick_entry.get(), self.phone_entry.get(), self.email_entry.get(), self.jvemail_entry.get(), self.address_entry.get(), self.city_entry.get(), self.statevar.get(), self.zip_entry.get(), self.birthday_entry.get(), self.faa_num_entry.get(), self.realtors_entry.get('1.0', tk.END), self.notes_entry.get('1.0', tk.END), self.emer_name_entry.get(), self.emer_relation_entry.get(), self.emer_cell_entry.get(), self.newabilities, first, last))

                c.execute('SELECT employee_id from photographers where first=? and last=?', (first, last))
                tar_id = str(c.fetchone()[0])
                print('tar_id is ' + tar_id)
                c.execute('DELETE from Coverage WHERE employee_id =?',(tar_id,))
                usertowns = self.userlistbox.get(0, tk.END)
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
                    #print('tar_cityid for ' + tartown + ' is ' + tar_cityid)
                    # print('state is ' + tarstate + '!   town is ' + tartown + '!   county is ' + tarcounty + '!')
                    c.execute('INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)', (tar_id, tar_cityid))

                conn.commit()
                print("Edits made to " + first + " " + last)
                
                if flag: #if there's been a change made to the name, update the name in the roster list
                    global rosterbox
                    index = rosterbox.index(tk.ACTIVE)
                    rosterbox.delete(index)
                    rosterbox.insert(index, self.fname_entry.get() + ' ' + self.lname_entry.get())
                    rosterbox.grid(row=1,column=0, padx=(20,0), rowspan=5, columnspan=2, sticky=tk.W+tk.N)
                editWindow.destroy()
            
            delbutton = ttk.Button(editWindow, text="Delete Photographer", command=lambda:confirm_removeGuy(self, first, last)).grid(row=5, column=0, padx=(30,0), pady=(10, 15), ipadx=8, sticky='nw')
            okbutton = ttk.Button(editWindow, text="Make Changes",  command=lambda:makeChanges(self)).grid(row=5, column=6, padx=(0,30), pady=(10, 15), ipadx=8, sticky='ne')
            
            

            def add_town():
                self.userlistbox.insert(tk.END, self.alltownbox.get(tk.ACTIVE))
                self.alltownbox.delete(tk.ACTIVE)
        
                
            def del_town():
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
        topFrame = tk.Frame(self, bd=2, width=500, relief=tk.RAISED,)
        topFrame.columnconfigure(0, weight=3)
        #topFrame.rowconfigure(0, weight=1)
        topFrame.grid(row=1, column=1, sticky='nw', rowspan=2, padx=15, pady=(0,5), ipadx=2)
        
        infoFrame = tk.Frame(topFrame, width=300)
        infoFrame.grid(row=0, column=0, rowspan=4, sticky='nws')
        
        
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
        buttons.grid(row=9, column=0, sticky='sw', rowspan=2, pady=(20, 5), padx=6)

        ttk.Button(buttons, text="Coverage", command=lambda:cov_popup(self.p_first.get(), self.p_last.get())).grid(row=0, column=0, sticky='ws', ipadx=2, padx=(0,5), pady=(10,0))
        ttk.Button(buttons, text="Emergency", command=lambda:emer_popup(self.p_first.get(), self.p_last.get())).grid(row=0, column=1, sticky='ws', ipadx=2, padx=(0,5), pady=(10,0))
        ttk.Button(buttons, text="Edit", command=lambda:editPop(self, self.p_first.get(), self.p_last.get())).grid(row=0,column=2, sticky='ws', ipadx=5, pady=(45,0))
        
        self.citylabel = tk.Label(infoFrame, text=self.p_city.get() +", " + self.p_state.get() + " " + self.p_zip.get())
        #self.citylabel.grid(row=1, column=3, sticky='es', padx=6)
        #tk.Button(checks, font=("TKDefaultFont", 8), text="Remove",bg="PINK", command=lambda:confirm_removeGuy(p_first.get(), p_last.get())).grid(row=9,  column=2, sticky='se', padx=(0,5), pady=6, ipadx=2)


        #services list
        services = tk.Frame(topFrame)
        services.columnconfigure(2, weight=1)
        services.grid(row=0, column=1, columnspan=2, sticky='ew')
        tk.Label(services, text="Services", font=("TKDefaultFont 8 bold")).grid(row=0, column=0, pady=(9,0), sticky='w')
        self.serviceList = tk.Listbox(services, width=15, height=8, activestyle='none')

        self.serviceList.grid(row=1, column=0, sticky='nsw')

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
        if (rosterbox.get(tk.ACTIVE) == ''):
            rosterbox.insert(tk.END, 'No Photographers!')
        else:
            viewProfile(self)
                
    ## DIVIDER
        #tk.Frame(self, height=1, width=500 ,bg="black").grid(row=2, column=1, columnspan=2, sticky=tk.N, pady=20)

    
    ## BOTTOM FRAME
        bottomFrame = tk.Frame(self,bd=2, relief=tk.RAISED)
        bottomFrame.grid(row=3, column=0, sticky='new', columnspan=2, pady=10, padx=15, ipadx=10, ipady=4)
        bottomFrame.columnconfigure(4, weight=1)
        tk.Label(bottomFrame, text="Search by City").grid(row=0, column=0, sticky=tk.W, pady=6, padx=6,)
        
        state_int = tk.IntVar()
        state_int.set(0)
        tk.Radiobutton(bottomFrame, text="NJ", variable=state_int, value="0", command=lambda:state_int.set(0)).grid(row=1, column=0)
        tk.Radiobutton(bottomFrame, text="NY", variable=state_int, value="1", command=lambda:state_int.set(1)).grid(row=1, column=1)
        tk.Radiobutton(bottomFrame, text="CT", variable=state_int, value="2", command=lambda:state_int.set(2)).grid(row=1, column=2)
        searchBox = tk.Entry(bottomFrame, width=25)
        searchBox.grid(row=0, column=1, columnspan=3, pady=6, sticky=tk.W+tk.E)
        
        
        def dupePop(results, city, state):
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
                picked = duperesultsBox.get(tk.ACTIVE)
                #print(picked)
                choice = picked.split(', ')
                choice[1] = choice[1].replace(' County', '')
                #print(choice)
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
            if len(townResults) > 1:
                dupePop(townResults, query.title(), searchstate)
                
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

                        if guy[4] != None: #if realtors isn't blank, append realtors
                            realtors = guy[4].replace('\n', ' ')
                            result += "    R: " + realtors
                        
                        if guy[5] != None: #if notes aren't blank, append notes
                            notes = guy[5].replace('\n', ' ')
                            result += "   N: " + notes
                        
                        resultsBox.insert(tk.END, result)
                        tk.Label(bottomFrame,text = (str(result_amt) + ' results')).grid(row=1, column=4, padx=(100, 0), sticky='es')
            
        def enterhit(event):
            searchcity(state_int)
        
        searchBox.bind("<Return>", enterhit)
            
        searchbutton = ttk.Button(bottomFrame, text="Search", command=lambda:searchcity(state_int))
        searchbutton.grid(row=0, column=4, padx=6, ipadx=10, sticky='w')
        
        resultsBox = tk.Listbox(bottomFrame, height=6, width=50)
        resultsBox.grid(row=2, column=0, pady=5, padx=(10, 0), columnspan=5, sticky='ew')
        resultsBox_scroll = tk.Scrollbar(bottomFrame, orient=tk.VERTICAL)
        resultsBox['yscrollcommand'] = resultsBox_scroll.set
        resultsBox_scroll['command'] = resultsBox.yview
        resultsBox_scroll.grid(row=2, column=5, padx=(0, 10), sticky='nsw')
        
        resultsBox_scroll2 = tk.Scrollbar(bottomFrame, orient=tk.HORIZONTAL)
        resultsBox['xscrollcommand'] = resultsBox_scroll2.set
        resultsBox_scroll2['command'] = resultsBox.xview
        resultsBox_scroll2.grid(row=3, column=0, sticky='news', columnspan=5)
    
    # def dragwin(self,event):
    #     x = self.winfo_pointerx() - self._offsetx
    #     y = self.winfo_pointery() - self._offsety
    #     self.geometry('+{x}+{y}'.format(x=x,y=y))

    # def clickwin(self,event):
    #     self._offsetx = event.x
    #     self._offsety = event.y    

        

          
### START PROGRAM
if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    app = root()
    app.mainloop()
    quit(1)
    

    

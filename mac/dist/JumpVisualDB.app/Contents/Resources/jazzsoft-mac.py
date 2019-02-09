import sqlite3
import os
import shutil
import hashlib
import tkinter as tk
from tkinter import ttk

## Created by John Gallino
## December, 2018

conn = sqlite3.connect('jump.db')
c = conn.cursor()
files = []
path = "photographers"
version = "v1.1 beta"

def parsePhone(phone):
    """ takes whatever fucked up phone number and formats it nice """
    numbers = ""
    for char in phone:
        if char.isdigit():
            numbers += char
    newphone = "(" + numbers[:3] + ') ' + numbers[3:6] + '-' + numbers[6:]
    return newphone

def clearPhotographers():
    c.execute("DELETE FROM photographers")
    conn.commit()
    
def checkColor(string):
    if u'\u2713' in string:
        return "GREEN"
    else:
        return "BROWN"
    
def readPhotographer(data, checksum):
    """ reads .jmp file and updates the database """
    data.seek(0,0)
    while True:
        name = data.readline()
        #break while loop if line is not a comment
        if not name.startswith('#'):
            break
    fullname = name.split(" ")
    firstname = fullname[0].title()
    lastname = fullname[1].rstrip('\n').title()
    #pull phone
    phone = data.readline().rstrip('\n')
    phone = parsePhone(phone)
    #pull email
    email = data.readline().rstrip('\n')
    #pull hometown
    city = data.readline().split(" ")
    hometown = city[0].rstrip('\n').title()
    homestate = city[1]
    slack = data.readline().rstrip('\n')
    abilities = data.readline().rstrip('\n')
    
     # writes contact info from .jmp file to photographer table in database
    c.execute("INSERT INTO photographers (first, last, phone, email, city, state, abilities, slack, checksum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (firstname, lastname, phone, email,  hometown, homestate, abilities, slack, checksum))
    
    # pulls out employee_ID for new photographer
    c.execute("SELECT employee_ID FROM photographers WHERE first=? AND last=?", (firstname, lastname))
    photoID = c.fetchone()
    photoID = str(photoID[0])
    #print(firstname + " " + lastname + "'s photoID is " + photoID)
    print(firstname + " " + lastname + " was added to the database.")
    # now reading coverage
    for line in data:
        if not line.startswith('\n'):
            try:
                line = line.split(" | ")
                county = line[0].title()
                town = line[1].title().rstrip('\n')
                #print("county is " + county + ". Town is " + town + ". For " + firstname + " " + lastname + ".")
                c.execute("SELECT id FROM USCities WHERE USCities.city=? AND county_name=?",(town.rstrip('\n'), county))
                townID = c.fetchone()
                townID = str(townID[0])
                #print("town id is " + townID)
                # writing employeeID + cityID into coverage table
                c.execute("INSERT INTO coverage (employee_id, city_id) VALUES (?, ?)", (photoID, townID)) 
            except:
                print("***ERROR - problem with the town " + town)
        else:
            continue
    print(firstname + " " + lastname + "'s coverage has been added to the database.\n")
    conn.commit()
    
def updatePhotographer(data, checksum):
    data.seek(0,0)
    while True:
        name = data.readline()
        #break while loop if line is not a comment
        if not name.startswith('#'):
            break
    fullname = name.split(" ")
    firstname = fullname[0].title()
    lastname = fullname[1].rstrip('\n').title()
    #pull phone
    origphone = data.readline().rstrip('\n')
    phone = parsePhone(origphone)
    #pull email
    email = data.readline().rstrip('\n')
    #pull hometown
    city = data.readline().split(" ")
    hometown = city[0].rstrip('\n').title()
    homestate = city[1]
    slack = data.readline().rstrip('\n')
    abilities = data.readline().rstrip('\n')
    
    c.execute("SELECT first, last, phone, email, city, state, slack, abilities, employee_id FROM photographers WHERE first=? AND last=?", (firstname, lastname))
    info = c.fetchone()
    targetid = info[8]
    if info[0] != firstname:
        print("info[0] is " + info[0] + " but firstname should be " + firstname)
        c.execute("UPDATE photographers SET first=? WHERE employee_id=?", (firstname, targetid))
    if info[1] != lastname:
        print("info[1] is " + info[1] + " but lastname should be " + firstname)
        c.execute("UPDATE photographers SET last=? WHERE employee_id=?", (lastname, targetid))
    if info[2] != phone:
        print("info[2] is " + info[2] + " but phone should be " + phone)
        c.execute("UPDATE photographers SET phone=? WHERE employee_id=?", (phone, targetid))
    if info[3] != email:
        print("info[3] is " + info[3] + " but email should be " + email)
        c.execute("UPDATE photographers SET email=? WHERE employee_id=?", (email, targetid))
    if info[4] != hometown:
        print("info[4] is " + info[4] + " but hometown should be " + hometown)
        c.execute("UPDATE photographers SET city=? WHERE employee_id=?", (hometown, targetid))
    if info[5] != homestate:
        print("info[5] is " + info[5] + " but homestate should be " + homestate)
        c.execute("UPDATE photographers SET state=? WHERE employee_id=?", (homestate, targetid))
    if info[6] != slack:
        print("info[6] is " + info[6] + " but slack should be " + slack)
        c.execute("UPDATE photographers SET slack=? WHERE employee_id=?", (slack, targetid))
    if info[7] != abilities:
        print("info[7] is " + info[7] + " but abilities should be " + abilities)
        c.execute("UPDATE photographers SET abilities=? WHERE employee_id=?", (abilities, targetid))
    
    #delete all coverage records for this photographer
        c.execute("DELETE FROM coverage WHERE employee_id=?", ([targetid]))
    #rewrite coverage records
        # now reading coverage
    for line in data:
        if not line.startswith('\n'):
            try:
                line = line.split(" | ")
                county = line[0].title()
                town = line[1].title().rstrip('\n')
                #print("county is " + county + ". Town is " + town + ". For " + firstname + " " + lastname + ".")
                c.execute("SELECT id FROM USCities WHERE USCities.city=? AND county_name=?",(town.rstrip('\n'), county))
                townID = c.fetchone()
                townID = str(townID[0])
                #print("town id is " + townID)
                # writing employeeID + cityID into coverage table
                c.execute("INSERT INTO coverage (employee_id, city_id) VALUES (?, ?)", (targetid, townID)) 
            except:
                print("***ERROR - problem with the town " + town)
        else:
            continue
        
    #update checksum
    c.execute("UPDATE photographers SET checksum=? WHERE employee_ID=?",(checksum, targetid))
    conn.commit()
    print(firstname + " " + lastname + "'s coverage has been updated.\n")

    
    
### ROOT SCREEN
class root(tk.Tk):
    """ JazzSoft root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      ##MAIN WINDOW  
        self.title("JumpVisual DB " + version)
        self.configure(bg="WHITE")
        #self.geometry("720x575")
        self.resizable(width=False, height=False)
        self.columnconfigure(1, weight=1)
        self.wm_iconbitmap('jvdb.ico')
        self.p_abilities = ''
    ## TOP IMAGE
        self.headimg = tk.PhotoImage(file="dispatch.pbm")
        tk.Label(self, bg="WHITE", image=self.headimg).grid(row=0, column=0, columnspan=10, sticky=tk.W+tk.E)
        #tk.Label(self, text=version).grid(row=0, column=0, sticky='sw')
    ## LEFT FRAME
        leftframe = tk.Label(self, bg="WHITE")
        leftframe.grid(row=1, column=0, sticky='nsw', rowspan=8)
        tk.Label(leftframe, text="Team Members", font=("TKDefaultFont", 14), bg="WHITE", fg="DARK RED").grid(row=0, column=0, sticky=tk.W+tk.N, padx=20)
        rosterbox = tk.Listbox(leftframe, width=20, height=20, activestyle='none', bd=2, font=("TKDefaultFont"))
        rosterbox_scroll = tk.Scrollbar(leftframe, orient=tk.VERTICAL)
        rosterbox['yscrollcommand'] = rosterbox_scroll.set
        rosterbox_scroll['command'] = rosterbox.yview
        rosterbox.grid(row=1,column=0, padx=20, rowspan=5, sticky=tk.W+tk.N)
        rosterbox_scroll.grid(row=1, column=0, rowspan=5, sticky=tk.N+tk.S+tk.E)
        tk.Label(leftframe, text=version, bg="WHITE", fg="GRAY").grid(row=7, column=0, padx=5, pady=6, sticky='swe')
        
        p_first = tk.StringVar()
        p_last = tk.StringVar()
        p_phone = tk.StringVar()
        p_email = tk.StringVar()
        p_slack = tk.StringVar()
        p_city = tk.StringVar()
        p_state = tk.StringVar()
        p_weekends = tk.StringVar()
        p_floor = tk.StringVar()
        p_mat = tk.StringVar()
        p_dusk = tk.StringVar()
        p_teaser = tk.StringVar()
        p_premium = tk.StringVar()
        p_luxury = tk.StringVar()
        p_vedit = tk.StringVar()
        p_aes = tk.StringVar()
        p_aev = tk.StringVar()
        p_faa = tk.StringVar()
        
        def viewProfile():
            """ Reads profile of the selected photographer """
            target = rosterbox.get(tk.ACTIVE).rstrip('\n')
            name = target.split(" ")
            p_first.set(name[0].title())
            p_last.set(name[1].rstrip('\n').title())
            c.execute("SELECT phone, email, city, state, slack, abilities FROM photographers WHERE first=? AND last=?", (p_first.get(), p_last.get()))
            info = c.fetchone()
            p_phone.set(info[0])
            p_email.set(info[1])
            p_city.set(info[2])
            p_state.set(info[3])
            p_slack.set(info[4])
            if '@' not in p_slack.get():
                p_slack.set('@'+p_slack.get())
            self.p_abilities = info[5].lower()
            updateProfileBox()

            
        for i in os.listdir(path):
            if i.endswith('.jmp'):
                files.append(i)
                
        print("files in '" + str(path) + "' folder are " + str(files))
        
        for file in files:
            moddate = os.stat("photographers/" +file)[8]
            # for each file in photographers folder, do checksum and pull the first and last name
            with open("photographers/" +file, "r") as data:
                checksum = hashlib.md5(open("photographers/"+file, "rb").read()).hexdigest()
                while True:
                    name = data.readline()
                    #break while loop if line is not a comment
                    if not name.startswith('#'):
                        
                        break
                fullname = name.split(" ")
                firstname = fullname[0].title()
                lastname = fullname[1].rstrip('\n').title()
                
                # check if this photographer is already in the database
                c.execute("SELECT employee_id FROM photographers WHERE first = ? AND last = ?", (firstname, lastname))
                check = c.fetchall()
                if len(check) ==0:
                    print("\n" + name.rstrip('\n').title() + " is not in database. Adding now...")
                    readPhotographer(data, checksum)
                else:
                    # compare .jmp checksum to old checksum
                    c.execute("SELECT checksum FROM photographers WHERE first = ? AND last = ?", (firstname, lastname))
                    checkold = str(c.fetchone()[0])
                    if checkold != checksum:
                        #print("checksum reads as " + checksum + " but on record it is " + checkold)
                        print("UPDATE: There seems to be a change in " + firstname + " " + lastname + "'s .jmp file! Updating now...")
                        updatePhotographer(data, checksum)
                    else:
                        print(firstname + " " + lastname + " is already in the db and up to date")
                    
                # this part just populates the roster box    
                while True:
                    line = data.readline()
                    #break while loop if line is not a comment
                    if not line.startswith('#'):
                        break
                rosterbox.insert(tk.END, name.title())
                data.close()
                
                #check if every photographer in db has a corresponding .jmp file
                
        
        c.execute("SELECT first, last FROM photographers")
        db_photographers = c.fetchall()
        for photographer in db_photographers:
            filename = photographer[0] + photographer[1] + ".jmp"
            exists = os.path.isfile('photographers/'+filename)
            if exists:
                print(filename + " found")
            else:
                print("Uh oh! No file found for " + photographer[0] + " " + photographer[1] + ". Deleting them from db...")
                c.execute("SELECT employee_id FROM photographers WHERE first=? AND last=?", (photographer[0], photographer[1]))
                targetid = str(c.fetchone()[0])
                print("targetid is " + targetid)
                c.execute("DELETE FROM coverage WHERE employee_id=?",[targetid])
                c.execute("DELETE FROM photographers WHERE employee_id=?",[targetid])
                conn.commit()
                print("Done. " + photographer[0] + " " + photographer[1] + " has been removed from the database.")

            
        tk.Button(leftframe, text="View Profile", font=("TKDefaultFont"), command=viewProfile).grid(row=6, column=0, ipadx=44, sticky=tk.N)
        
        def updateProfileBox():
            """ updates the dang ole profile box """
            self.namelabel.destroy()
            self.namelabel = tk.Label(topFrame, text=(p_first.get() + " " + p_last.get()), font=("TKDefaultFont", 14))
            self.namelabel.grid(row=1, column=0, sticky=tk.W, pady=2, padx=10)
            
            tk.Frame(topFrame,height=1, width=400 ,bg="black").grid(row=2, column=0, columnspan=3, sticky='we', pady=5, padx=10)
            
            self.phonelabel.destroy()
            self.phonelabel = tk.Label(topFrame, text=p_phone.get())
            self.phonelabel.grid(row=3, column=0, sticky=tk.W, pady=2, padx=10)
            
            self.emaillabel.destroy()
            self.emaillabel = tk.Label(topFrame, text=p_email.get())
            self.emaillabel.grid(row=4, column=0, sticky=tk.W, pady=2, padx=10)
            
            self.slacklabel.destroy()
            self.slacklabel = tk.Label(topFrame, text=p_slack.get())
            self.slacklabel.grid(row=5, column=0, sticky=tk.W, pady=2, padx=10)
            
            self.citylabel.destroy()
            self.citylabel = tk.Label(topFrame, text=p_city.get() +", " + p_state.get())
            self.citylabel.grid(row=1, column=2, sticky=tk.E, pady=2, padx=10)
            
            ab_check(self.p_abilities)
            self.weekendlabel.destroy()
            self.weekendlabel = tk.Label(topFrame, text=p_weekends.get(), fg=checkColor(p_weekends.get()))
            self.weekendlabel.grid(row=3, column=1, sticky=tk.W, pady=2, padx=6)
            
            self.floorlabel.destroy()
            self.floorlabel = tk.Label(topFrame, text=p_floor.get(), fg=checkColor(p_floor.get()))
            self.floorlabel.grid(row=4, column=1, sticky=tk.W, pady=2, padx=6)
            
            self.matlabel.destroy()
            self.matlabel = tk.Label(topFrame, text=p_mat.get(), fg=checkColor(p_mat.get()))
            self.matlabel.grid(row=5, column=1, sticky=tk.W, pady=2, padx=6)
            
            self.dusklabel.destroy()
            self.dusklabel = tk.Label(topFrame, text=p_dusk.get(), fg=checkColor(p_dusk.get()))
            self.dusklabel.grid(row=6, column=1, sticky=tk.W, pady=2, padx=6)
            
            self.teaserlabel.destroy()
            self.teaserlabel = tk.Label(topFrame, text=p_teaser.get(), fg=checkColor(p_teaser.get()))
            self.teaserlabel.grid(row=3, column=2, sticky=tk.W, pady=2, padx=6)
            
            self.premiumlabel.destroy()
            self.premiumlabel = tk.Label(topFrame, text=p_premium.get(), fg=checkColor(p_premium.get()))
            self.premiumlabel.grid(row=4, column=2, sticky=tk.W, pady=2, padx=6)
            
            self.luxurylabel.destroy()
            self.luxurylabel = tk.Label(topFrame, text=p_luxury.get(), fg=checkColor(p_luxury.get()))
            self.luxurylabel.grid(row=5, column=2, sticky=tk.W, pady=2, padx=6)
            
            self.veditlabel.destroy()
            self.veditlabel = tk.Label(topFrame, text=p_vedit.get(), fg=checkColor(p_vedit.get()))
            self.veditlabel.grid(row=6, column=2, sticky=tk.W, pady=2, padx=6)
            
            self.aeslabel.destroy()
            self.aeslabel = tk.Label(topFrame, text=p_aes.get(), fg=checkColor(p_aes.get()))
            self.aeslabel.grid(row=7, column=1, sticky=tk.W, pady=2, padx=6)
            
            self.aevlabel.destroy()
            self.aevlabel = tk.Label(topFrame, text=p_aev.get(), fg=checkColor(p_aev.get()))
            self.aevlabel.grid(row=7, column=2, sticky=tk.W, pady=2, padx=6)
            
            self.faalabel.destroy()
            self.faalabel = tk.Label(topFrame, text=p_faa.get(), fg=checkColor(p_faa.get()))
            self.faalabel.grid(row=8, column=1, sticky=tk.W, pady=2, padx=6)
    
    ## POPUP COVERAGE   
        def cov_popup(first, last):
            window = tk.Toplevel()
            window.title("Coverage for " + first + " " + last)
          
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
            
        def confirm_removeGuy(first, last):
            confirm = tk.Toplevel(padx=15, pady=15)
            confirm.title("Are you sure?")
            tk.Label(confirm, text="Are you sure you want to remove " + first + " " + last + "?").grid(row=0, columnspan=2, column=0, pady=(0,15), sticky='ew')
            
            def removeGuy(first, last):
                c.execute("SELECT employee_id FROM photographers WHERE first=? AND last=?", (first, last))
                targetid = str(c.fetchone()[0])
                print("targetid is " + targetid)
                c.execute("DELETE FROM coverage WHERE employee_id=?", [targetid])
                c.execute("DELETE FROM photographers WHERE employee_id=?", [targetid])
                conn.commit()
                if not os.path.exists('photographers/trash'):
                    os.makedirs('photographers/trash')
                shutil.move("photographers/" + first + last +".jmp", "photographers/trash/" +first+last+".jmp")
                print(first + " " + last + "'s profile and coverage has been deleted")
                confirm.destroy()
                rosterbox.delete(tk.ACTIVE)
                
            def cancel():
                confirm.destroy()
                
            tk.Button(confirm, text="Cancel", command=cancel).grid(row=1, column=1, ipadx=5, padx=(0, 50), sticky='w')
            tk.Button(confirm, text="Yes", command=lambda:removeGuy(first, last)).grid(row=1, column=0, ipadx=10, padx=(50, 10))
            
    ## TOP FRAME
        topFrame = tk.Frame(self, bd=2, relief=tk.RAISED,)
        topFrame.columnconfigure(0, weight=1)
        topFrame.rowconfigure(0, weight=1)
        topFrame.grid(row=1, column=1, sticky=tk.W, pady=10, padx=15, ipadx=2)
        
        self.namelabel = tk.Label(topFrame, text=(p_first.get() + " " + p_last.get()), font=("TKDefaultFont", 14))
        self.namelabel.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2, padx=6)
        self.phonelabel = tk.Label(topFrame, text=p_phone.get())
        self.phonelabel.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2, padx=6)
        self.emaillabel = tk.Label(topFrame, text=p_email.get())
        self.emaillabel.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2, padx=6)
        self.slacklabel = tk.Label(topFrame, text=p_slack.get())
        self.slacklabel.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2, padx=6)
        buttons = tk.Frame(topFrame)
        buttons.grid(row=7, column=0, sticky='sw', rowspan=2, pady=10, padx=6)
        tk.Button(buttons, text="View Coverage", bg="LIGHTSTEELBLUE", command=lambda:cov_popup(p_first.get(), p_last.get())).grid(row=0, column=0, sticky='w', ipadx=2)
        tk.Button(buttons, text="Remove", command=lambda:confirm_removeGuy(p_first.get(), p_last.get())).grid(row=0,  column=1, sticky='sw', padx=(25,0), ipadx=2)
        
        self.citylabel = tk.Label(topFrame, text=p_city.get() +", " + p_state.get())
        self.citylabel.grid(row=1, column=3, sticky='es', padx=6)
        
        self.weekendlabel = tk.Label(topFrame, text=p_weekends.get())
        self.weekendlabel.grid(row=3, column=2, sticky=tk.W, padx=6)
        self.floorlabel = tk.Label(topFrame, text=p_floor.get())
        self.floorlabel.grid(row=4, column=2, sticky=tk.W, padx=6)
        self.matlabel = tk.Label(topFrame, text=p_mat.get())
        self.matlabel.grid(row=5, column=2, sticky=tk.W, padx=6)
        self.dusklabel = tk.Label(topFrame, text=p_dusk.get())
        self.dusklabel.grid(row=6, column=2, sticky=tk.W, padx=6)
        self.aeslabel = tk.Label(topFrame, text=p_aes.get())
        self.aeslabel.grid(row=7, column=2, sticky=tk.W, padx=6)
        self.faalabel = tk.Label(topFrame, text=p_faa.get())
        self.faalabel.grid(row=8, column=2, sticky=tk.W, padx=6)
        
        self.teaserlabel = tk.Label(topFrame, text=p_teaser.get())
        self.teaserlabel.grid(row=3, column=3, sticky=tk.W, padx=6)
        self.premiumlabel = tk.Label(topFrame, text=p_premium.get())
        self.premiumlabel.grid(row=4, column=3, sticky=tk.W, padx=6)
        self.luxurylabel = tk.Label(topFrame, text=p_luxury.get())
        self.luxurylabel.grid(row=5, column=3, sticky=tk.W, padx=6)
        self.veditlabel = tk.Label(topFrame, text=p_vedit.get())
        self.veditlabel.grid(row=6, column=3, sticky=tk.W, padx=6)
        self.aevlabel = tk.Label(topFrame, text=p_aev.get())
        self.aevlabel.grid(row=7, column=3, sticky=tk.W, padx=6)
        
        
        
        def ab_check(abilities):
            """ reads and decyphers abilities code """
            
            if "fl" in str(abilities):
                p_floor.set(u'\u2713' + " Floorplans")
            else:
                p_floor.set(u'\u2718' + " Floorplans")
                
            if "w" in abilities:
                p_weekends.set(u'\u2713' + " Weekends")
            else:
                p_weekends.set(u'\u2718' + " Weekends")
                
            if "ma" in abilities:
                p_mat.set(u'\u2713' + " Matterport")
            else:
                p_mat.set(u'\u2718' + " Matterport")
                
            if "du" in abilities:
                p_dusk.set(u'\u2713' + " Dusk Photos")
            else:
                p_dusk.set(u'\u2718' + " Dusk Photos")
                
            if "tv" in abilities:
                p_teaser.set(u'\u2713' + " Teaser Video")
            else:
                p_teaser.set(u'\u2718' + " Teaser Video")
                
            if "pv" in abilities:
                p_premium.set(u'\u2713' + " Premium Video")
            else:
                p_premium.set(u'\u2718' + " Premium Video")
                
            if "lv" in abilities:
                p_luxury.set(u'\u2713' + " Luxury Video")
            else:
                p_luxury.set(u'\u2718' + " Luxury Video")
                
            if "ed" in abilities:
                p_vedit.set(u'\u2713' + " Video Editing")
            else:
                p_vedit.set(u'\u2718' + " Video Editing")
                
            if "aes" in abilities:
                p_aes.set(u'\u2713' + " Aerial Stills")
            else:
                p_aes.set(u'\u2718' + " Aerial Stills")
                
            if "aev" in abilities:
                p_aev.set(u'\u2713' + " Aerial Video")
            else:
                p_aev.set(u'\u2718' + " Aerial Video")
                
            if "faa" in abilities:
                p_faa.set(u'\u2713' + " FAA Certified")
            else:
                p_faa.set(u'\u2718' + " FAA Certified")
        
        ab_check(self.p_abilities)
        viewProfile()
                
    ## DIVIDER
        #tk.Frame(self, height=1, width=500 ,bg="black").grid(row=2, column=1, columnspan=2, sticky=tk.N, pady=20)

    
    ## BOTTOM FRAME
        bottomFrame = tk.Frame(self,bd=2, relief=tk.RAISED)
        bottomFrame.grid(row=3, column=1, sticky='new', pady=10, padx=15, ipadx=10, ipady=10)
        bottomFrame.columnconfigure(4, weight=1)
        tk.Label(bottomFrame, text="Search by City").grid(row=0, column=0, sticky=tk.W, pady=6, padx=6,)
        
        state_int = tk.IntVar()
        state_int.set(0)
        tk.Radiobutton(bottomFrame, text="NJ", variable=state_int, value="0", command=lambda:state_int.set(0)).grid(row=1, column=0)
        tk.Radiobutton(bottomFrame, text="NY", variable=state_int, value="1", command=lambda:state_int.set(1)).grid(row=1, column=1)
        tk.Radiobutton(bottomFrame, text="CT", variable=state_int, value="2", command=lambda:state_int.set(2)).grid(row=1, column=2)
        searchBox = tk.Entry(bottomFrame, width=25)
        searchBox.grid(row=0, column=1, columnspan=3, pady=6, sticky=tk.W+tk.E)
        
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
            c.execute("SELECT first, last, photographers.city, abilities FROM photographers LEFT JOIN coverage ON photographers.employee_ID=coverage.employee_ID LEFT JOIN USCities on coverage.city_id=UScities.id WHERE UScities.city = ? AND UScities.state_id=?", (query.title(), searchstate))
            whatigot = c.fetchall()
            if len(whatigot)==0:
                resultsBox.insert(tk.END, "Sorry, no results. Check your spelling?")
            else:
                for guy in whatigot:
                    if guy[2] == query.title():  
                        resultsBox.insert(tk.END, guy[0] + " " + guy[1] + " lives there." + "  ["+ guy[3]+"]")
                    else:
                        resultsBox.insert(tk.END, guy[0] + " " + guy[1] + "  ["+ guy[3]+"]")
            
        def enterhit(event):
            searchcity(state_int)
        
        searchBox.bind("<Return>", enterhit)
            
        searchbutton = tk.Button(bottomFrame, text="Search", command=lambda:searchcity(state_int))
        searchbutton.grid(row=0, column=4, padx=6, ipadx=10, sticky='w')
        
        resultsBox = tk.Listbox(bottomFrame, height=6, width=50)
        resultsBox.grid(row=2, column=0, pady=5, padx=(10, 0), columnspan=5, sticky='ew')
        resultsBox_scroll = tk.Scrollbar(bottomFrame, orient=tk.VERTICAL)
        resultsBox['yscrollcommand'] = resultsBox_scroll.set
        resultsBox_scroll['command'] = resultsBox.yview
        resultsBox_scroll.grid(row=2, column=5, padx=(0, 10), sticky='nsw')
        

        

          
### START PROGRAM
if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    app = root()
    app.mainloop()
    raise SystemExit()
    

    

import sqlite3
import os
import hashlib
import tkinter as tk
from tkinter import ttk

## Created by John Gallino
## December, 2018

conn = sqlite3.connect('jump.db')
c = conn.cursor()
files = []
path = "photographers"
version = "v1.1 alpha"

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
    hometown = city[0].title()
    homestate = city[1].rstrip('\n')
    slack = data.readline().rstrip('\n')
    abilities = data.readline().rstrip('\n')
    
     # writes contact info from .jmp file to photographer table in database
    c.execute("INSERT INTO photographers (first, last, phone, email, city, state, abilities, slack, checksum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (firstname, lastname, phone, email,  hometown, homestate, abilities, slack, checksum))
    
    # pulls out employee_ID for new photographer
    c.execute("SELECT employee_ID FROM photographers WHERE first=? AND last=?", (firstname, lastname))
    photoID = c.fetchone()
    photoID = str(photoID[0])
    print(firstname + " " + lastname + "'s photoID is " + photoID)
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
    
    
    
### ROOT SCREEN
class root(tk.Tk):
    """ JazzSoft root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      ##MAIN WINDOW  
        self.title("JazzSoft Dispatch | JumpVisual")
        self.geometry("675x575")
        self.resizable(width=False, height=False)
        self.columnconfigure(1, weight=1)
        self.wm_iconbitmap('jump_dispatch_wEu_2.ico')
        self.p_abilities = ''
    ## TOP IMAGE    
        tk.Label(self, bg="BLUE", height=4).grid(row=0, column=0, columnspan=10, sticky=tk.W+tk.E)
        tk.Label(self, text=version).place(x=585, y=60, anchor=tk.SW)
    ## LEFT FRAME
        leftframe = tk.Label(self)
        leftframe.grid(row=1, column=0, sticky=tk.W, rowspan=8)
        tk.Label(leftframe, text="Team Members", font=("TKDefaultFont", 14)).grid(row=0, column=0, sticky=tk.W+tk.S, padx=20)
        rosterbox = tk.Listbox(leftframe, width=20, height=18, activestyle='none', bd=2, font=("TKDefaultFont"))
        rosterbox_scroll = tk.Scrollbar(leftframe, orient=tk.VERTICAL)
        rosterbox['yscrollcommand'] = rosterbox_scroll.set
        rosterbox_scroll['command'] = rosterbox.yview
        
        p_first = tk.StringVar()
        p_last = tk.StringVar()
        p_phone = tk.StringVar()
        p_email = tk.StringVar()
        p_slack = tk.StringVar()
        p_city = tk.StringVar()
        p_state = tk.StringVar()
        p_floor = tk.StringVar()
        p_video = tk.StringVar()
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
            self.p_abilities = info[5]
            updateProfileBox()

            
        for i in os.listdir(path):
            if i.endswith('.jmp'):
                files.append(i)
                
        print("files in '" + str(path) + "' folder are " + str(files))
        
        for file in files:
            moddate = os.stat("photographers/" +file)[8]
            
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
                    checknew = str(c.fetchone()[0])
                    if checknew != checksum:
                        print("UPDATE: There seems to be a change in " + firstname + " " + lastname + "'s .jmp file! Updating now...")
                        #readPhotographer(data, checksum)
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
        
        rosterbox.grid(row=1,column=0, padx=20, rowspan=5, sticky=tk.W)
        rosterbox_scroll.grid(row=1, column=0, rowspan=5, sticky=tk.N+tk.S+tk.E)
        tk.Button(leftframe, text="     View Profile     ", bg="LIGHT BLUE", font=("TKDefaultFont"), command=viewProfile).grid(row=6, column=0, sticky=tk.N)
        
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
            self.citylabel.grid(row=1, column=1, sticky=tk.E, pady=2, padx=10)
            
            ab_check(self.p_abilities)
            self.floorlabel.destroy()
            self.floorlabel = tk.Label(topFrame, text=p_floor.get(), fg=checkColor(p_floor.get()))
            self.floorlabel.grid(row=3, column=1, sticky=tk.W, pady=2, padx=15)
            
            self.videolabel.destroy()
            self.videolabel = tk.Label(topFrame, text=p_video.get(), fg=checkColor(p_video.get()))
            self.videolabel.grid(row=4, column=1, sticky=tk.W, pady=2, padx=15)
            
            self.aeslabel.destroy()
            self.aeslabel = tk.Label(topFrame, text=p_aes.get(), fg=checkColor(p_aes.get()))
            self.aeslabel.grid(row=5, column=1, sticky=tk.W, pady=2, padx=15)
            
            self.aevlabel.destroy()
            self.aevlabel = tk.Label(topFrame, text=p_aev.get(), fg=checkColor(p_aev.get()))
            self.aevlabel.grid(row=6, column=1, sticky=tk.W, pady=2, padx=15)
            
            self.faalabel.destroy()
            self.faalabel = tk.Label(topFrame, text=p_faa.get(), fg=checkColor(p_faa.get()))
            self.faalabel.grid(row=7, column=1, sticky=tk.W, pady=2, padx=15)
    
    ## POPUP COVERAGE   
        def cov_popup(first, last):
            window = tk.Toplevel()
            window.title("Coverage for " + first + " " + last)
            #indow.geometry("300")
            
            boxframe = tk.Frame(window)
            boxframe.grid(row=1, column=0, padx=15, ipady=15)
            cov_box = tk.Listbox(boxframe, width=40, height=30)
            cov_box_scroll = tk.Scrollbar(boxframe, orient=tk.VERTICAL)
            cov_box.grid(row=1, column=0, pady=5, sticky='news')
            cov_box_scroll.grid(row=1, column=1, sticky='nws')
            cov_box['yscrollcommand'] = cov_box_scroll.set
            cov_box_scroll['command'] = cov_box.yview
            c.execute("SELECT UScities.state_id, UScities.city, UScities.county_name FROM UScities LEFT JOIN coverage ON UScities.id=coverage.city_id LEFT JOIN photographers ON coverage.employee_id=photographers.employee_id WHERE photographers.first=? AND photographers.last=?", (first, last,))
         #example: c.execute("SELECT first, last, photographers.city, abilities FROM photographers LEFT JOIN coverage ON photographers.employee_ID=coverage.employee_ID LEFT JOIN USCities on coverage.city_id=UScities.id WHERE UScities.city = ?", (query.title(),))
            cov_results = c.fetchall()
            cov_list=list()
            count = 0
            for result in cov_results:
                gix = (result[0] + " | " + result[1] + ", " + result[2] + " County")
                print("gix is " + gix)
                cov_list.append(gix)
                count += 1
            cov_list.sort()
            print(cov_list)
            for item in cov_list:
                item = str(item)
                cov_box.insert(tk.END, item)
            tk.Label(window, text= first + " " + last + " covers " + str(count) + " towns :").grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)
            
    ## TOP FRAME
        topFrame = tk.Frame(self, bd=2, relief=tk.RAISED,)
        topFrame.columnconfigure(0, weight=1)
        topFrame.rowconfigure(0, weight=1)
        topFrame.grid(row=1, column=1, sticky=tk.E, pady=10, padx=25, ipadx=20)
        
        self.namelabel = tk.Label(topFrame, text=(p_first.get() + " " + p_last.get()), font=("TKDefaultFont", 14))
        self.namelabel.grid(row=1, column=0, sticky=tk.W, pady=2, padx=10)
        self.phonelabel = tk.Label(topFrame, text=p_phone.get())
        self.phonelabel.grid(row=3, column=0, sticky=tk.W, pady=2, padx=10)
        self.emaillabel = tk.Label(topFrame, text=p_email.get())
        self.emaillabel.grid(row=4, column=0, sticky=tk.W, pady=2, padx=10)
        self.slacklabel = tk.Label(topFrame, text=p_slack.get())
        self.slacklabel.grid(row=5, column=0, sticky=tk.W, pady=2, padx=10)
        tk.Button(topFrame, text="View Coverage", bg="LAVENDER", command=lambda:cov_popup(p_first.get(), p_last.get())).grid(row=7, rowspan=3, column=0, sticky=tk.W+tk.S, pady=10, padx=10)
        
        self.citylabel = tk.Label(topFrame, text=p_city.get() +", " + p_state.get())
        self.citylabel.grid(row=1, column=1, sticky=tk.E, pady=2, padx=10)
        
        self.floorlabel = tk.Label(topFrame, text=p_floor.get())
        self.floorlabel.grid(row=3, column=1, sticky=tk.W, padx=15)
        self.videolabel = tk.Label(topFrame, text=p_video.get())
        self.videolabel.grid(row=4, column=1, sticky=tk.W, padx=15)
        self.aeslabel = tk.Label(topFrame, text=p_aes.get())
        self.aeslabel.grid(row=5, column=1, sticky=tk.W, padx=15)
        self.aevlabel = tk.Label(topFrame, text=p_aev.get())
        self.aevlabel.grid(row=6, column=1, sticky=tk.W, padx=15)
        self.faalabel = tk.Label(topFrame, text=p_faa.get())
        self.faalabel.grid(row=7, column=1, sticky=tk.W, padx=15)
        
        
        def ab_check(abilities):
            """ reads and decyphers abilities code """
            
            if "_Fl" in str(abilities):
                p_floor.set(u'\u2713' + " Floorplans")
            else:
                p_floor.set(u'\u2718' + " Floorplans")
                
            if "_V" in abilities:
                p_video.set(u'\u2713' + " Video")
            else:
                p_video.set(u'\u2718' + " Video")
                
            if "_AeS" in abilities:
                p_aes.set(u'\u2713' + " Aerial Stills")
            else:
                p_aes.set(u'\u2718' + " Aerial Stills")
                
            if "_AeV" in abilities:
                p_aev.set(u'\u2713' + " Aerial Video")
            else:
                p_aev.set(u'\u2718' + " Aerial Video")
                
            if "_FAA" in abilities:
                p_faa.set(u'\u2713' + " FAA Certified")
            else:
                p_faa.set(u'\u2718' + " FAA Certified")
        
        ab_check(self.p_abilities)
        viewProfile()
                
    ## DIVIDER
        #tk.Frame(self, height=1, width=500 ,bg="black").grid(row=2, column=1, columnspan=2, sticky=tk.N, pady=20)

    
    ## BOTTOM FRAME
        bottomFrame = tk.Frame(self,bd=0, relief=tk.SUNKEN)
        bottomFrame.grid(row=3, column=1, sticky='new', padx=25, ipadx=20, ipady=10, columnspan=10)
        tk.Label(bottomFrame, text="Search by City").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        state_int = tk.IntVar()
        state_int.set(0)
        print("state int is " + str(state_int.get()))
        tk.Radiobutton(bottomFrame, text="NJ", variable=state_int, value="0", command=lambda:state_int.set(0)).grid(row=1, column=0)
        tk.Radiobutton(bottomFrame, text="NY", variable=state_int, value="1", command=lambda:state_int.set(1)).grid(row=1, column=1)
        tk.Radiobutton(bottomFrame, text="CT", variable=state_int, value="2", command=lambda:state_int.set(2)).grid(row=1, column=2)
        searchBox = tk.Entry(bottomFrame, width=30)
        searchBox.grid(row=0, column=1, columnspan=4, sticky=tk.W+tk.E)
        
        def searchcity(state_int):
            if state_int.get()==0:
                searchstate = "NJ"
            elif state_int.get()==1:
                searchstate = "NY"
            else:
                searchstate = "CT"
            print("state int is " + str(state_int.get()) + " searchstate is " + searchstate)
            resultsBox.delete(0, tk.END)
            query = searchBox.get()
            print(query + " was searched")
            c.execute("SELECT first, last, photographers.city, abilities FROM photographers LEFT JOIN coverage ON photographers.employee_ID=coverage.employee_ID LEFT JOIN USCities on coverage.city_id=UScities.id WHERE UScities.city = ? AND UScities.state_id=?", (query.title(), searchstate))
            whatigot = c.fetchall()
            print(whatigot)
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
            
        searchbutton = tk.Button(bottomFrame, text="Search", command=searchcity)
        searchbutton.grid(row=1, column=3, sticky=tk.W+tk.E)
        
        resultsBox = tk.Listbox(bottomFrame, height=10, width=40)
        resultsBox.grid(row=2, column=0, pady=5, columnspan=4)
        

          
### START PROGRAM
if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    
    app = root()
    app.mainloop()
    quit(1)
    

    

import tkinter as tk
import config
import sqlite3
from tkinter import ttk
from jumpvisualdb import checkjumpdb


def writeNewGuy(user):
    """ Takes a user object and adds them to the database """
    conn = sqlite3.connect('jump.db')
    c = conn.cursor()
    with conn:
        print("Adding new photographer to jump.db...")
        c.execute("INSERT INTO photographers (first, last, phone, email, jv_email, address, city, state, zip, birthday, faa_num, abilities, emer_name, emer_rel, emer_cell) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user.firstname, user.lastname, user.phone, user.email, user.jvemail, user.address,  user.hometown, user.homestate, user.zip, user.birthday, user.faa_num, user.abilities, user.emer_name, user.emer_relation, user.emer_cell))
        conn.commit()
        c.execute("SELECT employee_ID FROM photographers WHERE first=? AND last=?", (user.firstname, user.lastname))
        empID = c.fetchone()
        empID = str(empID[0])
        print("ID of new photographer is " + str(empID))
        
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
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (empID, townID))
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
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (empID, townID))
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
                    c.execute("INSERT INTO Coverage (employee_ID, city_id) VALUES (?, ?)", (empID, townID))
                except:
    # ERROR SHOULD BE LOGGED TO LOG FILE
                    print("Error with", "CT |", county, "County", city)
            print("DONE.")
        conn.commit()

class FinalFrame(tk.Frame):

    def __init__(self, parent, user, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        checkjumpdb()
        #update sidebar
        
        self.header_string = "Finishing Up!"

        self.top_string = ("You're done! Check out the information below and make sure it's correct. When you hit the Confirm button, the new team member will be added to jump.db")
        

        self.header_label = tk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.top_string_label = tk.Label(self, text=self.top_string, justify="left", anchor=tk.W,
                                     font=("TKDefaultFont",10), wraplength=500)
        # Proof
        report = tk.Frame(self)
        report.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.proof = tk.Text(report, height=21, width=60)
        self.proof.tag_configure('proof', font='TKDefaultFont 10', lmargin1=3, justify='left')
        self.proof_scroll = tk.Scrollbar(report, orient=tk.VERTICAL)
        self.proof['yscrollcommand'] = self.proof_scroll.set
        self.proof_scroll['command'] = self.proof.yview
        self.proof_scroll.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)
        self.proof.insert(tk.END, "Name:\t" + user.firstname.title() + " " + user.lastname.title() + "\n", 'proof')
        self.proof.insert(tk.END, "Phone:\t" + user.phone + "\n", 'proof')
        self.proof.insert(tk.END, "Personal Email:\t" + user.email + "\n", 'proof')
        self.proof.insert(tk.END, "JumpVisual Email:\t" + user.jvemail + "\n", 'proof')
        self.proof.insert(tk.END, "Address:\t" + user.address + "\n", 'proof')
        self.proof.insert(tk.END, "City:\t" + user.hometown + ", " + user.homestate+ "\n", 'proof')
        self.proof.insert(tk.END, "Birthday:\t" + user.birthday + "\n", 'proof')
        self.proof.insert(tk.END, "FAA Cert#:\t" + user.faa_num + "\n", 'proof')
        self.proof.insert(tk.END, "Services:\t" + user.abilities + "\n", 'proof')
        self.proof.insert(tk.END, "Emergency Contact:\t{x} ({y}) {z}\n".format(x=user.emer_name, y=user.emer_relation, z=user.emer_cell), 'proof')
        self.proof.insert(tk.END, "\n### COVERAGE ZONE ###\n", 'proof')
        self.usertowns = user.nj_towns + user.ny_towns + user.ct_towns
        
        for town in self.usertowns:
            self.proof.insert(tk.END, town + "\n", 'proof')
        self.proof.config(state=tk.DISABLED)
        self.proof.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        nav = tk.Frame(self)
        nav.grid(row=5, column=0, sticky=tk.E)
        
        self.finlabelgood = tk.Label(report, fg="GREEN", text="Team Member successfully added to database! You may now close this wizard.", anchor=tk.W)
        self.finlabelbad = tk.Label(report, fg="RED", text="Uh oh! Something went wrong!", anchor=tk.W)

        self.export_button = ttk.Button(report, text="Confirm New Photographer", command=lambda:self.export(user))
        self.export_button.grid(row=2, column=1, sticky=tk.E, pady=10, ipadx=10)
        
        #back button
        self.back_button = ttk.Button(nav, text="<< Back", command=lambda:self.back(user, parent))
        self.back_button.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)

        #placing the widgets inside Frame1
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        self.top_string_label.grid(row=1, column=0, sticky=tk.W, columnspan=2, ipady=8)
        
    def export(self, user):
        try:
            writeNewGuy(user)
            self.finlabelgood.grid(row=2, column=0, sticky=tk.W)
        except IOError:
            print("Error: problem writing data to file")
            self.finlabelbad.grid(row=2, column=0, sticky=tk.W)
        except ValueError:
            print('Error: problem with the data entered')
        except:
            print("Error: some other error occured")
            self.finlabelbad.grid(row=2, column=0, sticky=tk.W)
        finally:
            user.name = (user.firstname + ' ' + user.lastname).title()
            config.newuser = user.name


    def back(self, user, parent):
        config.i -= 1
        config.drawframe(parent, user)
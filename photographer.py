"""A class to represent a staff photographer"""
import pickle

class Photographer():
    """A photographer on staff"""
    
    def __init__(self, fname, lname):
       """Create blank profile using first name and last name entered"""
       self.fname = fname
       self.lname = lname
       self.full_name = self.fname + ' ' + self.lname
       self.email = ''
       self.phone = ''
       self.address = ''
       self.slack = ''
       self.abilities='P'

    def fill_profile(self):
        """Queries the user for photographer profile info"""
        email = input("\nEmail address: ")
        self.email = email
        phone = input("Phone num: ")
        self.phone = phone
        slack = input("Slack Handle: ")
        self.slack = slack
        address = input("Address: ")
        self.address = address

        yesno = input("Do they do video? (y/n): ")
        while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
            print("\nPlease answer 'y' or 'n'!")
            yesno = input("Do they do video? (y/n): ")
        if yesno == 'y' or yesno == 'Y':
            self.abilities+='/V'
    
        yesno = input("Do they do aerial stills? (y/n): ")
        while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
            print("\nPlease answer 'y' or 'n'!")
            yesno = input("Do they do aerial stills? (y/n): ")
        if yesno == 'y' or yesno == 'Y':
            self.abilities+='/As'
            aerial=True

        if aerial == True:
            yesno = input("Do they do aerial video? (y/n): ")
            while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
                print("\nPlease answer 'y' or 'n'!")
                yesno = input("Do they do aerial video? (y/n): ")
            if yesno == 'y' or yesno == 'Y':
                self.abilities+='/Av'

        if aerial == True:
            yesno = input("Are they currently FAA certified? (y/n): ")
            while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
                print("\nPlease answer 'y' or 'n'!")
                yesno = input("Are they currently FAA certified? (y/n): ")
            if yesno == 'y' or yesno == 'Y':
                self.abilities+='/Af'

        yesno = input("Do they do Matterport? (y/n): ")
        while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
            print("\nPlease answer 'y' or 'n'!")
            yesno = input("Do they do Matterport? (y/n): ")
        if yesno == 'y' or yesno == 'Y':
            self.abilities+='/M'     

        yesno = input("Do they do floorplans? (y/n): ")
        while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
            print("\nPlease answer 'y' or 'n'!")
            yesno = input("Do they do floorplans? (y/n): ")
        if yesno == 'y' or yesno == 'Y':
            self.abilities+='/Fl'
        
    
    # def edit_profile(self, attribute):
    #     """Edits the profile attribute passed by the user"""
        
    #     if attribute == "1":
    #         self.fname = input("Enter new first name: ")
    #         self.lname = input("Enter new last name: ")
    #         #with open(filename, 'wb') as f_obj:
    #             #pickle.dump(photographers, f_obj)
    #         print("Edit completed and written to file. Press Enter to continue.")
    #         input()
    #     elif attribute == "2":
    #         self.email = input("Enter new email: ")
    #         print("Edit completed and written to file. Press Enter to continue.")
    #         input()
    #     elif attribute == "3":
    #         self.phone = input("Enter new phone number: ")
    #         print("Edit completed and written to file. Press Enter to continue.")
    #         input()
    #     elif attribute == "4":
    #         self.address = input("Enter new address: ")
    #         print("Edit completed and written to file. Press Enter to continue.")
    #         input()
    #     elif attribute == "5":
    #         self.slack = input("Enter new slack handle: ")
    #         print("Edit completed and written to file. Press Enter to continue.")
    #         input()
    #     elif attribute == "6":
    #         yesno = input("Change video attribute to (y/n): ")
    #         while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
    #             print("\nPlease answer 'y' or 'n'!")
    #             yesno = input("Do they do video? (y/n): ")
    #         if yesno == 'y' or yesno == 'Y':
    #             self.video = True
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #         elif yesno == 'n' or yesno == 'N':
    #             self.video = False
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #     elif attribute == "7":
    #         yesno = input("Change floorplan attribute to (y/n): ")
    #         while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
    #             print("\nPlease answer 'y' or 'n'!")
    #             yesno = input("Do they do floorplans? (y/n): ")
    #         if yesno == 'y' or yesno == 'Y':
    #             self.video = True
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #         elif yesno == 'n' or yesno == 'N':
    #             self.video = False
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #     elif attribute == "8":
    #         yesno = input("Change aerial attribute to (y/n): ")
    #         while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
    #             print("\nPlease answer 'y' or 'n'!")
    #             yesno = input("Do they do aerial photography? (y/n): ")
    #         if yesno == 'y' or yesno == 'Y':
    #             self.video = True
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #         elif yesno == 'n' or yesno == 'N':
    #             self.video = False
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #     elif attribute == "9":
    #         yesno = input("Change FAA Certified attribute to (y/n): ")
    #         while yesno != 'y' and yesno != 'Y' and yesno != 'n' and yesno != 'N':
    #             print("\nPlease answer 'y' or 'n'!")
    #             yesno = input("Are they currently FAA certified? (y/n): ")
    #         if yesno == 'y' or yesno == 'Y':
    #             self.video = True
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #         elif yesno == 'n' or yesno == 'N':
    #             self.video = False
    #             print("Edit completed and written to file. Press Enter to continue.")
    #             input()
    #     else:
    #         attribute = input("Not a valid option! Try again: ")
    #         self.edit_profile(attribute)
       
    
    def get_profile(self):
        """Return a neatly formated profile of the photographer"""
        profile = '    Name: ' + self.full_name.title() + '\n    Email: ' + self.email + '\n    Phone: ' + self.phone + '\n    Address: ' + self.address + '\n    Slack: ' + self.slack + '\n\n    Video: ' + str(self.video) + '\n    Floorplan: ' + str(self.floorplan) + '\n    Aerial: ' + str(self.aerial) + '\n    FAA Certified: ' + str(self.faa_cert)
        return profile
    
    def get_profile_to_edit(self):
        """Return a neatly formated profile of the photographer"""
        profile = '1.    Name: ' + self.full_name.title() + '\n2.    Email: ' + self.email + '\n3.    Phone: ' + self.phone + '\n4.    Address: ' + self.address + '\n5.    Slack: ' + self.slack + '\n\n6.    Video: ' + str(self.video) + '\n7.    Floorplan: ' + str(self.floorplan) + '\n8.    Aerial: ' + str(self.aerial) + '\n9.    FAA Certified: ' + str(self.faa_cert)
        return profile

import tkinter as tk
from tkinter import ttk

version = "v1.0"

### USER CLASS
class User():
	"""A class to hold the User's data"""
	
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)

		print("A user has been created")
		self.firstname = 'Bob'
		self.lastname = 'Fakeguy'
		self.email = ''
		self.phone = ''
		self.address = ''
		self.slack = ''
		self.abilities = 'P'
		self.nj_bool = False
		self.ny_bool = False
		self.ct_bool = False
		self.nj_counties = []
		self.ny_counties = []
		self.ct_counties = []

class Wizard():
	""" JumpVisual Wizard root window """
	

	def create_frame1(self, u):
		'''create frame 1'''
		self.Frame1 = tk.Frame(self.root)
		self.header_string = "Welcome to the JumpVisual Coverage Wizard!"

		self.top_string = ("This simple program is intended for JumpVisual staff photographers. It will help you "
						"choose the towns that you want (or do not want) to cover, and "
						"generate a report at the end to input into our database."
						"\n\nLet's get started!")

		header_label = ttk.Label(self.Frame1, text=self.header_string, anchor=tk.W,
								 font=("TKDefaultFont", 24), wraplength=500)
		top_string_label = ttk.Label(self.Frame1, text=self.top_string, anchor=tk.W,
									 font=("TKDefaultFont", 16), wraplength=500)

		ttk.Label(self.Frame1, text="First Name:").grid(row=2, column=0, ipady=20, sticky=tk.W)
		ttk.Label(self.Frame1, text=u.firstname).grid(row=2,column=1,ipady=20, sticky=tk.W)

		next_button = ttk.Button(self.Frame1, text="Next >>", command=self.create_frame2(u))

		#placing the widgets inside Frame1
		self.Frame1.grid(row=0, column=0)
		header_label.grid(row=0, column=0, sticky=tk.W)
		top_string_label.grid(row=1, column=0, sticky=tk.W, ipady=20)
	
		next_button.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)

	def create_frame2(self, u):
		'''create frame 2'''
		Frame2 = tk.Frame(self.root)
		ttk.Label(Frame2, text = "Frame 2 here!").grid(row=5, column=1)



	def app(self, u):
		'''create root window'''
		self.root = tk.Tk()
		self.root.title("JumpVisual Photographer Coverage Wizard")
		self.root.geometry("800x600")
		self.root.resizable(width=False, height=False)

		self.create_frame1(u)
		self.root.mainloop()
	

if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

	user1 = User()
	wiz = Wizard()
	wiz.app(user1)
	exit()

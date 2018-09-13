"""Main placeholder frame for wizard"""
import tkinter as tk
from tkinter import ttk

class HelloView(tk.Frame):
    """A friendly little module"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = tk.StringVar() #create a StringVar called name
        self.hello_string = tk.StringVar() #create a StringVar called hello_string
        self.hello_string.set("Hello World") #set hello_string to "Hello World"

        name_label = ttk.Label(self, text="Name:") #creates a label we'll refer to as name_label
        name_entry = ttk.Entry(self, textvariable=self.name) #creates an entry box 'name_entry' with textvariable that will store the entry as name

        ch_button = ttk.Button(self, text="Change", 
            command=self.on_change) #creates a 'Change' button that executes the on_change function when pressed

        hello_label = ttk.Label(self, textvariable=self.hello_string,
            font=("TkDefaultFont", 64), wraplength=600) #creates a Label that says whatever hello_string is set to, in big fuckin letters

        # now we'll actually place all the shit we just created
        name_label.grid(row=0, column=0, sticky=tk.W)
        name_entry.grid(row=0, column=1, sticky=(tk.W + tk.E))
        ch_button.grid(row=0, column=2, sticky=tk.E)
        hello_label.grid(row=1, column=0, columnspan=3)

        self.columnconfigure(1, weight=1) #this gives weight to the second column, making it expand horizontally and squish the first and third columns

    def on_change(self):
        if self.name.get().strip(): #if self.name contains any characters (minus whitespace)
            self.hello_string.set("Hello " + self.name.get())
        else:
            self.hello_string.set("Hello World")

class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hello Tkinter")
        self.geometry("800x600")
        self.resizable(width=False, height=False)

        HelloView(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)

if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()
    app = MyApplication()
    app.mainloop()

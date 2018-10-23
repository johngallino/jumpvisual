import tkinter as tk
from tkinter import ttk

class Frame1(tk.Frame):

    def __init__(self, parent,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "Welcome to the JumpVisual Coverage Wizard!"
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(self, text="Next >>", command=lambda:app.drawframe(frames[1])).grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)
        
class Frame2(tk.Frame):

    def __init__(self, parent,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "This is Frame 2!"
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        
        
class Frame3(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_string = "This is Frame 3!"
        self.header_label = ttk.Label(self, text=self.header_string, anchor=tk.W,
                                 font=("TKDefaultFont", 16), wraplength=500)
        self.header_label.grid(row=0, column=0, sticky=tk.W)
        

frames = [Frame1, Frame2, Frame3]
limit = len(frames)
i=0

class Wizard(tk.Tk):
    """ JumpVisual Wizard root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("JumpVisual Photographer Coverage Wizard")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.current_frame = frames[i](self, padx=30, pady=30, width=400)

        
    def drawframe(self, frame):
        """draws current frame"""
        print("i is " + str(i) + " limit is " + str(limit))
        self.current_frame.grid(row=0,column=1)
        

if __name__ == '__main__': #if this file is being run directly from the terminal (instead of from another py script), run mainloop()

    
    app = Wizard()
    app.drawframe(frames[0])
    app.mainloop()
    exit()



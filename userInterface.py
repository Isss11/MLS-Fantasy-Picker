from tkinter import ttk
from tkinter import messagebox
from tkinter import *

class UserInterface:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("MLS Fantasy Picker")
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindowHandler)
        
    # set-up frame and elements
    def startApplication(self):
        self.mainframe = ttk.Frame(self.root)
        
        # now adding main elements
        title = ttk.Label(self.mainframe, text="MLS Fantasy Picker")
                
        # adding elements to frame(s)
        self.mainframe.grid(column=0, row=0, sticky=N)
        title.grid(column=0, row=0, sticky=N)
        
        ui.root.mainloop()
        
    def closeWindowHandler(self):
        # protocol handler for closing a window
        if messagebox.askyesno("Close Application - Confirmation", "Are you sure you want to close this application?"):
            self.root.destroy()
    
if __name__ == "__main__":
    ui = UserInterface()
    ui.startApplication()
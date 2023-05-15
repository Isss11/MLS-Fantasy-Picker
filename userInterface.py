from tkinter import *
from tkinter import ttk

class UserInterface:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("MLS Fantasy Picker")
        self.root.mainloop()
        
        self.setUp()
    # set-up frame and elements
    def setUp(self):
        self.frame = ttk.Frame(self.root)
        
        # now adding main elements
        title = ttk.Label(self.root, text="MLS Fantasy Picker")
                
        self.frame.grid(column=0, row=0)
        title.grid(column=0, row=0)
if __name__ == "__main__":
    ui = UserInterface()
    ui.setUp()
# This is a GUI to control the Quantos
#
# University of Liverpool
# Autonomous Chemistry Laboratory
#
# (C) 2020 Lewis Jones <Lewis.Jones@liverpool.ac.uk>

from mettler_toledo_quantos import MettlerToledoDevice
from tkinter import *


# Here, we are creating our class, Window, and inheriting from the Frame class
class Window(Frame):

    # Define settings upon initialisation. From here we can specify
    def __init__(self, master=None):

        # parameters to be sent to the frame class
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # then run init_window, which is written below
        self.init_window()

    # creation of init_window
    def init_window(self):

        # Changing title of master widget
        self.master.title('Quantos GUI')

        # Allowing widget to take full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Creating a button instance
        quitButton = Button(self, text='Quit', command=self.client_exit)

        # Placing button on window
        quitButton.place(x=0,y=0)

    # creation of function to exit window
    def client_exit(self):
        exit()

# root window created
root = Tk()

# Size of the window
root.geometry('400x300')

# creation of an instance
app = Window(root)

#mainloop
root.mainloop()
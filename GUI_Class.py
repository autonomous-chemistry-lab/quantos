#! /Users/lewisjones/PycharmProjects/Quantos_devel/venv/bin/python
# A GUI used to create an xml file of vials and masses, readable by a secondary script to send commands to a
# Mettler-Toledo Quantos to enable dispensing.
#
# University of Liverpool
# Materials Innovation Factory
# Autonomous Chemistry Laboratory
#
# (C) 2020 Lewis Jones <Lewis.Jones@liverpool.ac.uk>


from tkinter import *
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import time


class QuantosGUI:
    def __init__(self, master):
        # Set master
        self.master = master

        # Setting the title of master widget
        master.title('Quantos Dispensing')

        # Introductory message
        self.intro_message = 'Please enter the mass (in mg) to be dispensed below.'
        self.label = Label(master, text=self.intro_message, font='helvetica 16 bold', pady=5)
        self.label.grid(row=0, column=0, columnspan=4)

        # Create table headings
        self.vial_label = Label(master, text='Vial', font='helvetica 14 bold')
        self.vial_label.grid(row=1, column=1)
        self.mass_label = Label(master, text='Mass', font='helvetica 14 bold')
        self.mass_label.grid(row=1,column=2)

        # Create vial labels
        for i in range(20):
            Label(master, text=str(i + 1), font='helvetica 14').grid(row=i + 2, column=1)

        # Create quit button
        self.quit_button = Button(master, text='Quit', command=self.client_exit)
        self.quit_button.grid(row=22,column=1)

        # Create send button
        self.send_button = Button(master, text='Send', command=self.get_values)
        self.send_button.grid(row=22, column=2)

        # Creating entries for each vial
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        self.e7 = Entry(master)
        self.e8 = Entry(master)
        self.e9 = Entry(master)
        self.e10 = Entry(master)
        self.e11 = Entry(master)
        self.e12 = Entry(master)
        self.e13 = Entry(master)
        self.e14 = Entry(master)
        self.e15 = Entry(master)
        self.e16 = Entry(master)
        self.e17 = Entry(master)
        self.e18 = Entry(master)
        self.e19 = Entry(master)
        self.e20 = Entry(master)

        # Create list of entries for later commands
        self.e_list = [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7, self.e8, self.e9, self.e10,
                       self.e11, self.e12, self.e13, self.e14, self.e15, self.e16, self.e17, self.e18, self.e19, self.e20]

        # Place each entry on the GUI
        self.e1.grid(row=2, column=2)
        self.e2.grid(row=3, column=2)
        self.e3.grid(row=4, column=2)
        self.e4.grid(row=5, column=2)
        self.e5.grid(row=6, column=2)
        self.e6.grid(row=7, column=2)
        self.e7.grid(row=8, column=2)
        self.e8.grid(row=9, column=2)
        self.e9.grid(row=10, column=2)
        self.e10.grid(row=11, column=2)
        self.e11.grid(row=12, column=2)
        self.e12.grid(row=13, column=2)
        self.e13.grid(row=14, column=2)
        self.e14.grid(row=15, column=2)
        self.e15.grid(row=16, column=2)
        self.e16.grid(row=17, column=2)
        self.e17.grid(row=18, column=2)
        self.e18.grid(row=19, column=2)
        self.e19.grid(row=20, column=2)
        self.e20.grid(row=21, column=2)

        # Initialise menubar
        self.menubar = Menu(master)

        # Create file menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Clear Values', command=self.clear_values)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.client_exit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        # Create help menu
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About', command=self.about_msg)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        # Add menubar to main window
        master.config(menu=self.menubar)

    # Methods
    def print_hello(self):
        '''
        Debugging command that prints Hello to commandline
        '''
        print('Hello World!')

    def clear_values(self):
        '''
        Function to clear all entries
        '''
        for e in self.e_list:
            e.delete(0, 5)

    def about_msg(self):
        '''
        Creation of a popup message in 'About' menu bar with information about what the GUI does and the developer
        '''
        self.popup = Tk()
        self.popup.wm_title("About")
        self.msg = 'A program to create xml files for sending to a Mettler-Toledo Quantos Automatic Solid Dispenser\n' \
              'for remote dispensing\n\n' \
              'Lewis Jones\n Lewis.Jones@liverpool.ac.uk\n' \
              'Autonomous Chemistry Laboratory\n' \
              'Universtity of Liverpool\n 2020'
        self.about_label = Label(self.popup, text=self.msg)
        self.about_label.pack(side="top", fill="x", pady=10)
        self.B1 = Button(self.popup, text="OK", command=self.popup.destroy)
        self.B1.pack()
        self.popup.mainloop()

    def client_exit(self):
        '''
        Exits the program
        '''
        exit()

    def get_values(self):
        '''
        Gets values from GUI and saves them into a dictionary
        '''
        # Create empty list for inputted mass values from GUI
        self.vals_list = []
        # A list containing each vial name
        self.vials = ['Vial 1', 'Vial 2', 'Vial 3', 'Vial 4', 'Vial 5', 'Vial 6', 'Vial 7', 'Vial 8', 'Vial 9',
                      'Vial 10', 'Vial 11', 'Vial 12', 'Vial 13', 'Vial 14', 'Vial 15', 'Vial 16', 'Vial 17',
                      'Vial 18', 'Vial 19', 'Vial 20']

        # Loop through each entry in e_list and append values to vals_list, adding '0' if empty
        for e in self.e_list:
            if e.get() == '':
                self.vals_list.append(0)
            else:
                self.vals_list.append((e.get()))

        # Create dictionary
        self.vals_dict = dict(zip(self.vials, self.vals_list))



if __name__ == '__main__':
    root = Tk()
    my_gui = QuantosGUI(root)
    root.mainloop()

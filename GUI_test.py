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
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import time


'''Creation of Main Widget functions'''
# creation of function to exit window
def client_exit():
    exit()

def show_amounts():
    # Create empty list for inputted mass values from GUI
    vals_list = []

    # A list containing each vial name, used in creating the dictionary
    vials = ['Vial 1', 'Vial 2', 'Vial 3', 'Vial 4', 'Vial 5', 'Vial 6', 'Vial 7', 'Vial 8', 'Vial 9', 'Vial 10',
             'Vial 11', 'Vial 12', 'Vial 13', 'Vial 14', 'Vial 15', 'Vial 16', 'Vial 17', 'Vial 18', 'Vial 19',
             'Vial 20']

    # List of entry boxes from GUI to extract the inputted values from
    e_list = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20]

    # Loop through each entry in e_list and append values to vals_list, adding '0' if empty
    for e in e_list:
        if e.get() == '':
            vals_list.append(0)
        else:
            vals_list.append((e.get()))

    # Create dictionary
    vals_dict = dict(zip(vials, vals_list))

    # Turn dictionary into an xml file
    xml = dicttoxml(vals_dict, custom_root='quantos', attr_type=False).decode('utf-8')  # attr_type used to remove 'type' from xml

    # To create a 'prettified' xml
    dom = parseString(xml)
    pretty_xml = dom.toprettyxml()

    # write entries from GUI into xml file called 'Values.xml'
    with open('Values.xml', 'w') as f:
        f.write(pretty_xml)


'''Enhancing 'Send' button to include a popup message acknowledging completion and clearing values'''
# Creating popup window
def sent_msg():
    popup = Tk()
    popup.wm_title("!")
    msg_1 = 'Values sent'
    label = Label(popup, text=msg_1)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# Combining previous 'Send' command with clearing the entries and showing popup
def send_clear_popup():
    show_amounts()
    time.sleep(0.5)
    clear_entry()
    time.sleep(0.5)
    sent_msg()


'''Creation of menu bar'''
# create function that clears entries
def clear_entry():
    for e in e_list:
        e.delete(0,5)

# Creation of a popup message in 'About' menu bar with information about what the GUI does and the developer
def about_msg():
    popup = Tk()
    popup.wm_title("About")
    msg = 'A program to create xml files for sending to a Mettler-Toledo Quantos Automatic Solid Dispenser\n' \
          'for remote dispensing\n\n' \
          'Lewis Jones\n Lewis.Jones@liverpool.ac.uk\n' \
          'Autonomous Chemistry Laboratory\n' \
          'Universtity of Liverpool\n 2020'
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()


'''Initialising main tkinter window'''
# set 'master' as a tkinter instance
master = Tk()

# Setting the title of master widget
master.title('Quantos Dispensing')

# changing theme of GUI
style = ThemedStyle(master)
style.set_theme('scidgrey')                     # use ttk.Button etc to access the themes

# intro message
intro_message = 'Please enter the mass (in mg) to be dispensed below.'
Label(master, text=intro_message, font='helvetica 16 bold', pady=5).grid(row=0, column=0, columnspan=4)

# create 'Send' button
ttk.Button(master,
       text='Send',
       command=send_clear_popup).grid(row=22, column=2)

# Creating a quit button instance
quitButton = ttk.Button(master, text='Quit', command=client_exit)

# Placing quit button on window
quitButton.grid(row=22,column=1)

# Creating vial labels and placing them in grid
Label(master, text='Vial', font='helvetica 14 bold').grid(row=1, column=1)
Label(master, text='Mass', font='helvetica 14 bold').grid(row=1,column=2)

# creating labels for the different vials
for i in range(20):
    Label(master, text=str(i+1), font='helvetica 14').grid(row=i+2, column=1)

# Creating entries attached to variables, to use get() function on
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)
e10 = Entry(master)
e11 = Entry(master)
e12 = Entry(master)
e13 = Entry(master)
e14 = Entry(master)
e15 = Entry(master)
e16 = Entry(master)
e17 = Entry(master)
e18 = Entry(master)
e19 = Entry(master)
e20 = Entry(master)

# Generate list of entry values for easy access
e_list = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20]

# Place each entry on the GUI
e1.grid(row=2, column=2)
e2.grid(row=3, column=2)
e3.grid(row=4, column=2)
e4.grid(row=5, column=2)
e5.grid(row=6, column=2)
e6.grid(row=7, column=2)
e7.grid(row=8, column=2)
e8.grid(row=9, column=2)
e9.grid(row=10, column=2)
e10.grid(row=11, column=2)
e11.grid(row=12, column=2)
e12.grid(row=13, column=2)
e13.grid(row=14, column=2)
e14.grid(row=15, column=2)
e15.grid(row=16, column=2)
e16.grid(row=17, column=2)
e17.grid(row=18, column=2)
e18.grid(row=19, column=2)
e19.grid(row=20, column=2)
e20.grid(row=21, column=2)


'''Initialising menu bar'''
# initialise menu
menubar = Menu(master)

# file menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Clear Values', command=clear_entry)
filemenu.add_separator()
filemenu.add_command(label='Quit', command=client_exit)
menubar.add_cascade(label='File', menu=filemenu)

# help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=about_msg)
menubar.add_cascade(label='Help', menu=helpmenu)


'''Finalise window'''
master.config(menu=menubar)
master.mainloop()


'''Next step is to create a __main__ and wrap the above into a main() function'''
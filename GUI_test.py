#! /Users/lewisjones/PycharmProjects/Quantos_devel/venv/bin/python
# This is a GUI to control the Quantos
#
# University of Liverpool
# Autonomous Chemistry Laboratory
#
# (C) 2020 Lewis Jones <Lewis.Jones@liverpool.ac.uk>

from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

master = Tk()

# Changing title of master widget
master.title('Quantos Dispensing')

# hex colour
hex = '#676a6e'

# change background colour
#master.configure(bg=hex)

# changing theme of GUI
style = ThemedStyle(master)
style.set_theme('scidgrey')                     # use ttk.Button etc to access the themes

# creation of function to exit window
def client_exit():
    exit()

# Creating a quit button instance
quitButton = ttk.Button(master, text='Quit', command=client_exit)

# Placing quit button on window
quitButton.grid(row=22,column=1)

# intro message
intro_message = 'Please enter the mass (in mg) to be dispensed below.'
Label(master, text=intro_message, font='helvetica 16 bold', pady=5).grid(row=0, column=0, columnspan=4)

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

def show_amounts():
    # Create empty list for values from GUI
    vals_list = []

    # lists of vials for creating dictionary
    vials = ['Vial 1','Vial 2','Vial 3','Vial 4','Vial 5','Vial 6','Vial 7','Vial 8','Vial 9','Vial 10',
             'Vial 11','Vial 12','Vial 13','Vial 14','Vial 15','Vial 16','Vial 17','Vial 18','Vial 19','Vial 20']

    # list of entries from GUI to extract digits from
    e_list = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20]

    # loop through each entry and append values as integers to values_list, adding 0 if empty
    for e in e_list:
        if e.get() == '':
            vals_list.append(0)
        else:
            vals_list.append((e.get()))

    # Create dictionary
    vals_dict = dict(zip(vials, vals_list))

    '''
    text1 = 'Vial 1 = {}\nVial 2 = {}\nVial 3 = {}\nVial 4 = {}\nVial 5 = {}\nVial 6 = {}\nVial 7 = {}' \
            '\nVial 8 = {}\nVial 9 = {}\nVial 10 = {}\nVial 11 = {}\nVial 12 = {}\nVial 13 = {}' \
            '\nVial 14 = {}\nVial 15 = {}\nVial 16 = {}\nVial 17 = {}\nVial 18 = {}\nVial 19 = {}\nVial 20 = {}'
            
    print(text1.format(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(),
                       e6.get(), e7.get(), e8.get(), e9.get(), e10.get(),
                       e11.get(), e12.get(), e13.get(), e14.get(), e15.get(),
                       e16.get(), e17.get(), e18.get(), e19.get(), e20.get()))
    '''
    # debug creation of dictionary
    #print(vals_dict)

    # Turn dictionary into an xml file
    xml = dicttoxml(vals_dict, custom_root='quantos', attr_type=False).decode('utf-8')          # attr_type is to remove 'type' from xml

    # to create prettified xml
    dom = parseString(xml)
    pretty_xml = dom.toprettyxml()

    # write entries from GUI into xml file
    with open('Values.xml', 'w') as f:
        f.write(pretty_xml)

ttk.Button(master,
       text='Send',
       command=show_amounts).grid(row=22, column=2)

master.mainloop()

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


class QuantosGUI:
    def __init__(self, master):
        self.master = master

        # Setting the title of master widget
        master.title('Quantos Dispensing')

        # Introductory message
        intro_message = 'Please enter the mass (in mg) to be dispensed below.'
        self.label = Label(master, text=intro_message, font='helvetica 16 bold', pady=5)
        self.label.grid(row=0, column=0, columnspan=4)

        # Create table headings
        self.vial_label = Label(master, text='Vial', font='helvetica 14 bold')
        self.vial_label.grid(row=1, column=1)
        self.mass_label = Label(master, text='Mass', font='helvetica 14 bold')
        self.mass_label.grid(row=1,column=2)



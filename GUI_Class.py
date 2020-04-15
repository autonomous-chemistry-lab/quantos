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


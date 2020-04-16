# mettler_toledo_quantos

This Python package (mettler_toledo_quantos) creates a class named
MettlerToledoDevice, to interface to Mettler Toledo Quantos using the Mettler 
Toledo Quantos Command Set as defined in the reference manual.

This package also creates a class named GUI_Class, which is a graphical
user interface (GUI) used for generating an XML file containing information 
about how much of a reagent is to be dispensed into each sample vial.

# Installation

# Usage
Upon running GUI_Class.py, the main GUI window will be opened. There are 20
entry boxes which relate to the 20 sample vials to be dispensed.

## Entering Values
1) Enter the desired masses in milligrams (mg) into each entry box
2) Click 'Send' button

### Send Button
The 'Send' button triggers the ```self.send_button_command()```, 
which does a number of tasks:
1) All entry values are read as strings into variables ```self.e1-self.e20```
2) A dictionary ```self.vals_dict``` is generated containing the vial
number and the mass of reagent to be dispensed into each vial
3) ```self.create_xml()``` converts ```self.vals_dict``` into an xml
file, titled 'new_values.xml'
4) The entry values are cleared using ```self.clear_values()```
5) A popup window telling the user that the XML file has been created
is shown

### Quit Button
This button closes the GUI and terminates the program.

## Menubar
### Clearing values
File > Clear Values

This removes any values in the entry boxes.

### Show 'About' information
Help > About

This tells the user what the GUI is used for and gives information
about the developers.
 

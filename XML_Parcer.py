'''
First attempt at XML parcer using Element Tree

University of Liverpool
Autonomous Chemistry Lab

Lewis Jones <lewis.jones@liverpool.ac.uk>
'''

'''
Importing ElementTree module
'''
import xml.etree.ElementTree as ET

'''
Reading .xml file from directory
'''
tree = ET.parse('test_xml.xml')
root = tree.getroot()

'''
Testing .xml file
'''
#print(root.tag)
#print(root.attrib)

"""
Iterate over each line and print the 'id' tag and its value
"""
#for child in root:
    #print(child.tag, child.attrib)

for vial in root.findall('vial'):
    if vial.get('id') == '1':
        mass = vial.find('mass').text
        print(mass)
        break

    elif vial.get('id') == '2':
        mass = vial.find('mass').text
        print(mass)
        break

'''Popup Loaded with an Image'''

import os
import PySimpleGUI as sg

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) 
sg.popup("Hello Instagram!", image=CURRENT_WORKING_DIRECTORY + "\\instagram.png")

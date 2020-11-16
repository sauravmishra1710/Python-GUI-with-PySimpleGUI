'''YES NO POPUP WITH CUSTOM ICON'''

import os
import PySimpleGUI as sg

# cwd = os.getcwd()
# script = os.path.realpath(__file__)

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
# getcwd() API is not returning the exact path.

sg.popup_yes_no('Popup with Yes No Buttons. The default icon for this popup is also changed.',
                title='Yes_No_Popup_With_Icon', icon=CURRENT_WORKING_DIRECTORY + "\\popup.ico")

'''File Open Popup'''

import sys
import PySimpleGUI as sg

if len(sys.argv) == 1:
    FILE_NAME = sg.popup_get_file('Choose File...')
else:
    FILE_NAME = sys.argv[1]

if not FILE_NAME:
    sg.popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
else:
    sg.popup('The file you chose is -', FILE_NAME, title="Selected File")

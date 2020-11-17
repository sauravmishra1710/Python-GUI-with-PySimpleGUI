'''POPUP_GET_DATE - POPUP TO SELECT DATE FROM A CALENDAR PICK'''

import datetime
import PySimpleGUI as sg

LAYOUT = [[sg.Text("Select Date:")],
          [sg.InputText(size=(40, 1), key='-TEXT-', disabled=True),
           sg.Button('Select Date', key='-DATE-', tooltip='Select Date')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the window
WINDOW = sg.Window('Date Select', LAYOUT)

# Display and interact with the Window using an Event Loop
while True:
    EVENT, VALUES = WINDOW.read()

    # check if user wants to quit or window was closed
    if EVENT in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    if EVENT == '-DATE-':
        DATE = sg.popup_get_date()

    DATE = datetime.datetime(DATE[2], DATE[0], DATE[1])

    # print(date.strftime("%b %d %Y %H:%M:%S"))
    # Display the selected date
    WINDOW['-TEXT-'].update(DATE.strftime("%b %d %Y"))

# Finish up by removing from the screen
WINDOW.close()

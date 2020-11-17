'''Pupup to get text.'''

import PySimpleGUI as sg

LAYOUT = [[sg.Text("User Text:")],
          [sg.InputText(size=(40, 1), key='-USER_TEXT-', disabled=True),
           sg.Button('Enter Text', key='-TEXT-', tooltip='Get User Text')],
          [sg.Button('OK', key='-OK-'), sg.Button('Cancel', key='-Cancel-')]]

# Create the window
WINDOW = sg.Window('Date Select', LAYOUT)

# Display and interact with the Window using an Event Loop
while True:
    EVENT, VALUES = WINDOW.read()

    # check if user wants to quit or window was closed
    if EVENT in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    if EVENT == '-TEXT-':
        TEXT = sg.popup_get_text('Enter Text')
        WINDOW['-USER_TEXT-'].update(TEXT)

    if EVENT == '-OK-':
        WINDOW.close()

# Finish up by removing from the screen
WINDOW.close()

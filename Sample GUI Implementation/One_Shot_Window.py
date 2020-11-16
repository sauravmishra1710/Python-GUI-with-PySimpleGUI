'''A Simple GUI Login Popup.'''

import PySimpleGUI as sg

# Define the window layout which consists of a username label,
# input text box, a password label and a password textbox where the
# input characters are masked.
LAYOUT = [[sg.Text("Name:")],
          [sg.Input(key='-INPUT-')],
          [sg.Text('Password:')],
          [sg.InputText('', key='Password', password_char='*')],
          [sg.Button('OK'), sg.Button('Cancel')]]

# Create the window
WINDOW = sg.Window('Login', LAYOUT)

# Display and interact with the Window using an Event Loop.
# When a button is clicked, the click event returns the text
# of the button clicked by the user.
while True:
    EVENT, VALUES = WINDOW.read()
    # See if user wants to quit or window was closed
    if EVENT in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    # if the user clicks OK, display a message with login success.
    # No validation is added at this point as this is purely to
    # introduce the GUI concepts.
    if EVENT == 'OK':
        sg.Popup('SUCCESS! (This is to ensure that the message is\
                 long enough for the popup title to be visible)',
                 title='Login Result', modal=True)

# Finish up by removing from the screen
WINDOW.close()

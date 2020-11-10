import PySimpleGUI as sg

# Define the window layout which consists of a username label,
# input text box, a password label and a password textbox where the
# input characters are masked.
layout = [[sg.Text("Name:")],
          [sg.Input(key='-INPUT-')],
          [sg.Text('Password:')],
          [sg.InputText('', key='Password', password_char='*')],
          [sg.Button('OK'), sg.Button('Cancel')]]

# Create the window
window = sg.Window('Login', layout)

# Display and interact with the Window using an Event Loop. 
# When a button is clicked, the click event returns the text 
# of the button clicked by the user.
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    
    # if the usre clicks OK, display a message with login success. 
    # No validation is added at this point as this is purely to 
    # introduce the GUI concepts.
    if event == 'OK':
        sg.Popup('Login Result', 'SUCCESS!', modal = True)
    
# Finish up by removing from the screen
window.close()
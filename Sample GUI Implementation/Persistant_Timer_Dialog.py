import PySimpleGUI as sg
from datetime import datetime

timer_paused = False
layout = [[sg.Text('')],
[sg.Text(size=(16,2),key='text')],
[sg.Button('Pause',key='Pause'),sg.Button('Resume',key='Resume'), sg.Exit(key='Exit')]]

window = sg.Window('Timer', layout, size=(300, 120), modal=True)

while True:

    # For more details on non-blobking window events and the usage of 'timeout' parameter
    # read @ https://github.com/PySimpleGUI/PySimpleGUI/issues/520
    # Read with a timeout is a very good thing for your GUIs to use in a read non-blocking situation, 
    # if you can use them. If your device can wait for a little while, then use this kind of read. 
    # The longer you're able to add to the timeout value, the less CPU time you'll be taking).
    # window.read(timeout=10) : This program will quickly test for user input, then deal with the hardware. 
    # Then it'll sleep for 10ms, while your gui is non-responsive, then it'll check in with your GUI again.
    event, values = window.read(timeout=10)

    # Close window if exit.\/close is clicked.
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    window['text'].update(current_time)

    # Pause the timer.
    if event == 'Pause':
        timer_paused = True
    
    if timer_paused == True:
        window['text'].update('Timer Paused')
    
    # Resume the timer.
    if event == 'Resume':
        timer_paused = False
        window['text'].update(current_time)

# Finish up by removing from the screen
window.close()
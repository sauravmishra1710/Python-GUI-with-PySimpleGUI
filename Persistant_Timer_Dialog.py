import PySimpleGUI as sg
from datetime import datetime

timer_paused = False
layout = [[sg.Text('')],
[sg.Text(size=(16,2),key='text')],
[sg.Button('Pause',key='Pause'),sg.Button('Resume',key='Resume'), sg.Exit(key='Exit')]]

window = sg.Window('Timer', layout, size=(300, 120), modal=True)

while True:
    event, values = window.read(timeout=10)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    window['text'].update(current_time)

    if event == 'Pause':
        timer_paused = True
    
    if timer_paused == True:
        window['text'].update('Timer Paused')
    
    if event == 'Resume':
        timer_paused = False
        window['text'].update(current_time)
# Finish up by removing from the screen
window.close()
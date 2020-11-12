import PySimpleGUI as sg
import time

# Change the default look and feel / theme of the window.
sg.ChangeLookAndFeel('Black')
sg.SetOptions(element_padding=(2, 2))
  
layout = [[sg.Text('')],  
         [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],  
         [sg.ReadButton('Pause', key='button', button_color=('white', '#001480')),  
          sg.ReadButton('Reset', button_color=('white', '#007339'), key='Reset'),  
          sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]  
  
window = sg.Window('Running Timer', no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True).Layout(layout)
  
current_time = 0  
stop_watched_paused = False  
start_time = int(round(time.time() * 100))

# start the window event loop
while (True): 

    # For more details on non-blobking window events and the usage of 'timeout' parameter
    # read @ https://github.com/PySimpleGUI/PySimpleGUI/issues/520
    # Read with a timeout is a very good thing for your GUIs to use in a read non-blocking situation, 
    # if you can use them. If your device can wait for a little while, then use this kind of read. 
    # The longer you're able to add to the timeout value, the less CPU time you'll be taking).
    # window.read(timeout=10) : This program will quickly test for user input, then deal with the hardware. 
    # Then it'll sleep for 10ms, while your gui is non-responsive, then it'll check in with your GUI again.
    if not stop_watched_paused:
        event, values = window.read(timeout=10)
        current_time = int(round(time.time() * 100)) - start_time
    else:
        event, values = window.Read() 

    # this is to flex between the Pause/Resume the stop watch. We work with the button text to trigger
    # the required concerned event.
    if event == 'button':
        event = window.FindElement(event).GetText()

    # Close window if exit is pressed.
    if event == 'Exit':
        break
    
    # Reset the stop watch timer.
    if event == 'Reset':
        start_time = int(round(time.time() * 100))
        current_time = 0

    # Pause the stop watch timer.
    if event == 'Pause':
        stop_watched_paused = True
        paused_time = int(round(time.time() * 100))
        window.FindElement('button').update(text='Resume')

    # Resume the stop watch timer event.
    if event == 'Resume':
        stop_watched_paused = False
        start_time = start_time + int(round(time.time() * 100)) - paused_time
        window.FindElement('button').update(text='Pause')

    # Read and update window
    #current_time = int(round(time.time() * 100)) - start_time 

    # Display timer in window
    window.FindElement('text').Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,  
                                                                  (current_time // 100) % 60,  
                                                                  current_time % 100))

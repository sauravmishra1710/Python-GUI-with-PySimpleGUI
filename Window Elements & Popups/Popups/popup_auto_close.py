import PySimpleGUI as sg

AUTO_CLOSE_TIME = 10
sg.popup_auto_close('This popup will close in ' + str(AUTO_CLOSE_TIME) + ' seconds.', title='Auto Close Popup', auto_close_duration=AUTO_CLOSE_TIME)
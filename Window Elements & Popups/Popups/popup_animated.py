'''ANIMATED POPUP'''

import PySimpleGUI as sg

for i in range(100000):
    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, title='Animated Popup',
                      no_titlebar=False, background_color='white', time_between_frames=100)

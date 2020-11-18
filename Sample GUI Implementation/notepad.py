'''A simple Notepad application implemented using PySimpleGUI.'''
# pylint: disable=no-member
# pylint: disable=invalid-name

import wx
import PySimpleGUI as sg

# change the default theme.
sg.theme('dark grey 9')

WINDOW_WIDTH: int = 90
WINDOW_HEIGHT: int = 25
FILE_NAME: str = None
DEFAULT_FONT_NAME: str = 'Times New Roman'

def ShowFontDialog():
    app=[]
    app = wx.App(None)
    # app = Font()
    # app.MainLoop()
    dialog = wx.FontDialog(None, wx.FontData())
    if dialog.ShowModal() == wx.ID_OK:
        data = dialog.GetFontData()
        font = data.GetChosenFont()
        font_info = font.GetNativeFontInfoUserDesc()

        styles = [style for style in font_info.split(' ')]
        underline = font.GetUnderlined()
        colour = data.GetColour()
        

# string variables to shorten loop and menu code
file_new: str = 'New             (CTRL+N)'
file_open: str = 'Open           (CTRL+O)'
file_save: str = 'Save           (CTRL+S)'

menu_layout: list = [['&File', [file_new, file_open, file_save, 'Save As', '__________________', 'Exit']],
                     ['&Statistics', ['Word Count', 'Character With Spaces', 'Character Without Spaces', ]],
                     ['&Help', ['About']]]

layout: list = [[sg.Menu(menu_layout)],
                [sg.Text('New File:', font=(DEFAULT_FONT_NAME, 10), size=(WINDOW_WIDTH, 1), key='-FILE_INFO-')],
                [sg.Multiline(font=(DEFAULT_FONT_NAME, 12, 'underline italic'), size=(WINDOW_WIDTH, WINDOW_HEIGHT), key='-BODY-')]]

WINDOW = sg.Window('Notepad', layout=layout, margins=(0, 0),
                   resizable=True, return_keyboard_events=True)
WINDOW.read(timeout=1)
WINDOW.maximize()
WINDOW['-BODY-'].expand(expand_x=True, expand_y=True)

def new_file() -> str:
    ''' Reset body and info bar, and clear FILE_NAME variable '''
    WINDOW['-BODY-'].update(value='')
    WINDOW['-FILE_INFO-'].update(value='New File:')

def open_file() -> str:
    ''' Open file and update the infobar '''
    try:
        file_name = sg.popup_get_file('Open File', no_window=True)
    except: # pylint: disable=bare-except
        return
    if file_name not in (None, '') and not isinstance(file_name, tuple):
        with open(file_name, 'r') as f:
            WINDOW['-BODY-'].update(value=f.read())
        WINDOW['-FILE_INFO-'].update(value=file_name)
    return file_name

def save_file(file_name: str):
    ''' Save file instantly if already open; otherwise display `save-as` popup '''

    file_name = WINDOW['-FILE_INFO-'].DisplayText # pylint: disable=no-member # Get the filename if already saved in the same session.
    if file_name not in (None, '', 'New File:'):
        with open(file_name, 'w') as f:
            f.write(VALUES.get('-BODY-'))
        WINDOW['-FILE_INFO-'].update(value=file_name)
    else:
        save_as()

def save_as() -> str:
    ''' Save new file or save existing file with another name '''
    try:
        file_name: str = sg.popup_get_file('Save As', save_as=True, no_window=True)
    except: # pylint: disable=bare-except
        return
    if file_name not in (None, '') and not isinstance(FILE_NAME, tuple):
        with open(file_name, 'w') as f:
            f.write(VALUES.get('-BODY-'))
        WINDOW['-FILE_INFO-'].update(value=file_name)
    return file_name

def get_word_count():
    ''' Get the estimated word count '''
    words: list = [word for word in VALUES['-BODY-'].split(' ') if word != '\n']
    word_count: int = len(words)
    return word_count

def character_count():
    '''Get the total number of characters in the file.'''
    chars = len(VALUES['-BODY-']) - 1
    return chars

def characters_without_spaces():
    '''Get the total number of characters in the file.'''

    chars_without_spaces: int = 0
    # total number of spaces is 1 less than the number of words.
    total_spaces: int = get_word_count() - 1

    if total_spaces == -1:
        chars_without_spaces = character_count()
    else:
        chars_without_spaces = character_count() - total_spaces

    return chars_without_spaces

def about():
    '''About the application'''

    sg.PopupQuick('A simple Notepad like application created using\
        PySimpleGUI framework.', auto_close=False)

while True:
    EVENT, VALUES = WINDOW.read()

    if EVENT in (None, 'Exit'):
        break
    if EVENT in (file_new, 'n:78'):
        FILE_NAME = new_file()
    if EVENT in (file_open, 'o:79'):
        FILE_NAME = open_file()
    if EVENT in (file_save, 's:83'):
        save_file(FILE_NAME)
    if EVENT in ('Save As',):
        FILE_NAME = save_as()   
    if EVENT in ('Word Count',):
        WORDS = get_word_count()
        sg.PopupQuick('Word Count: {:,d}'.format(WORDS), auto_close=False)
    if EVENT in ('Characters With Spaces',):
        TOTAL_CHARS = character_count()
        sg.PopupQuick('Characters With Spaces: {:,d}'.format(TOTAL_CHARS), auto_close=False)
    if EVENT in ('Character Without Spaces',):
        CHAR_WITHOUT_SPACES = characters_without_spaces()
        sg.PopupQuick('Characters Without Spaces: {:,d}'.format(CHAR_WITHOUT_SPACES), auto_close=False)
    if EVENT in ('About',):
        # about()
        ShowFontDialog()
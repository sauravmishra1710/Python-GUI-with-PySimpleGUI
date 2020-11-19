'''A simple Notepad application implemented using PySimpleGUI.'''
# pylint: disable=no-member
# pylint: disable=invalid-name

import shlex
import wx
import PySimpleGUI as sg

# change the default theme.
sg.theme('dark grey 9')

WINDOW_WIDTH: int = 90
WINDOW_HEIGHT: int = 25
FILE_NAME: str = None
font_dict = {}
DEFAULT_FONT_NAME: str = 'Times New Roman'

def ShowFontDialog():
    '''Get a font dialog to display and return all the
    font settings chosen to be applied to the editor.'''

    # the font styles supported by PySimpleGUI are mentioned
    # @ https://github.com/PySimpleGUI/PySimpleGUI/issues/3633#issuecomment-729675676
    # bold, italic, underline, and overstrike. These styles can be specified as a
    # string like - 'overstrike underline italic'

    wx_app = [] # pylint: disable=unused-variable
    wx_app = wx.App(None)

    font_style_modifier: str = ''

    dialog = wx.FontDialog(None, wx.FontData())
    if dialog.ShowModal() == wx.ID_OK:
        data = dialog.GetFontData()
        font = data.GetChosenFont()

        font_info = font.GetNativeFontInfoUserDesc()
        selected_styles = shlex.split(font_info)

        if 'bold' in selected_styles:
            font_style_modifier += 'bold '

        if 'italic' in selected_styles:
            font_style_modifier += 'italic '

        if font.GetUnderlined():
            font_style_modifier += 'underline '

        if font.GetStrikethrough():
            font_style_modifier += 'overstrike '

        font_color = data.GetColour()
        font_color = rgb2hex(font_color[0], font_color[1], font_color[2])

        font_facename = font.GetFaceName()

        font_size = font.GetPointSize()

        WINDOW['-BODY-'].update(font=(font_facename, font_size, font_style_modifier),
                                text_color=font_color)


def rgb2hex(r, g, b):
    '''Convert RGB to hex values.'''
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

# string variables to shorten loop and menu code
file_new: str = 'New             (CTRL+N)'
file_open: str = 'Open           (CTRL+O)'
file_save: str = 'Save           (CTRL+S)'

menu_layout: list = [['&File', [file_new, file_open, file_save, 'Save As', '__________________', 'Exit']],
                     ['&Statistics', ['Word Count', 'Line Count', 'Character With Spaces', 'Character Without Spaces', ]],
                     ['F&ormat', ['Font', ]],
                     ['&Help', ['About']]]

layout: list = [[sg.Menu(menu_layout)],
                [sg.Text('New File:', font=('Times New Roman', 10),
                         size=(WINDOW_WIDTH, 1), key='-FILE_INFO-')],
                [sg.Multiline(font=(DEFAULT_FONT_NAME, 12),
                              size=(WINDOW_WIDTH, WINDOW_HEIGHT), key='-BODY-')]]

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

    # Get the filename if already saved in the same session.
    file_name = WINDOW['-FILE_INFO-'].DisplayText
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
    total_words: int = 0
    if not validate_text():
        sg.PopupQuick('Enter some text to calculate the number of words.',
                      title='Text Not Found', auto_close=False)
        return 0

    lines: list = VALUES['-BODY-'].splitlines()
    for line in lines:
        words = line.split()
        total_words += len(words)

    return total_words

def validate_text() -> bool:
    '''validates if the user has entered some text in the note body
    and returns True/False accordingly.'''

    user_text: str = VALUES['-BODY-']
    if user_text == '\n':
        return False
    else:
        return True

def character_count():
    '''Get the total number of characters in the file.'''

    if not validate_text():
        sg.PopupQuick('Enter some text to calculate the number of characters.',
                      title='Text Not Found', auto_close=False)
        return 0

    chars = len(VALUES['-BODY-']) - 1
    return chars

def characters_without_spaces():
    '''Get the total number of characters in the file.'''

    if not validate_text():
        sg.PopupQuick('Enter some text to calculate the number of characters\nwithout spaces.',
                      title='Text Not Found', auto_close=False)
        return 0

    chars_without_spaces: int = 0
    # total number of spaces is 1 less than the number of words.
    total_spaces: int = get_word_count() - 1

    if total_spaces == -1:
        chars_without_spaces = character_count()
    else:
        chars_without_spaces = character_count() - total_spaces

    return chars_without_spaces

def get_line_count():
    ''' Get the estimated line count '''

    if not validate_text():
        sg.PopupQuick('Enter some text to calculate the number of lines.',
                      title='Text Not Found', auto_close=False)
        return 0

    text: str = VALUES['-BODY-']

    # extract the lines in the editor body. '\n' is the line separator
    # so we use it to split the text. The last line ends with '\n' which
    # includes an extra empty string ('') entry adding +1 to the total lines.
    # so we strip the last new line ('\n') character.
    lines: list = [line for line in text.rstrip('\n').split('\n')]
    # lines: list = text.splitlines() # can also be used.
    line_count: int = len(lines)
    return line_count

def about():
    '''About the application'''

    sg.PopupQuick('A simple Notepad like application created using\
        PySimpleGUI framework.', auto_close=False)

# read the events and take appropriate actions.
while True:
    EVENT, VALUES = WINDOW.read()

    if EVENT in (sg.WINDOW_CLOSED, 'Exit'):
        # exit out of the application is close or exit clicked.
        break
    if EVENT in (file_new, 'n:78'):
        new_file()
    if EVENT in (file_open, 'o:79'):
        FILE_NAME = open_file()
    if EVENT in (file_save, 's:83'):
        save_file(FILE_NAME)
    if EVENT in ('Save As',):
        FILE_NAME = save_as()
    if EVENT in ('Word Count',):
        WORDS = get_word_count()
        if WORDS != 0:
            sg.PopupQuick('Word Count: {:,d}'.format(WORDS), auto_close=False)
    if EVENT in ('Line Count',):
        LINES = get_line_count()
        if LINES != 0:
            sg.PopupQuick('Line Count: {:,d}'.format(LINES), auto_close=False)
    if EVENT in ('Character With Spaces',):
        CHARS = character_count()
        if CHARS != 0:
            sg.PopupQuick('Characters With Spaces: {:,d}'.format(CHARS), auto_close=False)
    if EVENT in ('Character Without Spaces',):
        CHAR_WITHOUT_SPACES = characters_without_spaces()
        if CHAR_WITHOUT_SPACES != 0:
            sg.PopupQuick('Characters Without Spaces: {:,d}'.format(CHAR_WITHOUT_SPACES),
                          auto_close=False)
    if EVENT in ('About',):
        about()
    if EVENT in ('Font',):
        ShowFontDialog()

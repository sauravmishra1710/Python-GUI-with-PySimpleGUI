'''IMAGE VIEWER

PySimpleGUI reads images in PNG, GIF, PPM/PGM format.
JPEGs cannot be shown because tkinter does not naively support these formats.
JPEGs can be converted to PNG format using the Python Imaging Library (PIL)
package prior to viewing them using PySimpleGUI package.

Sample code for conversion from JPEG/JPG to PNGs is hsown in the commented code block below.

extension = values["image_file"].lower().split(".")[-1]
if extension in ["jpg", "jpeg"]:  # JPG file
    new_filename = values["image_file"].replace(extension, "png")
    im = Image.open(values["image_file"])
    im.save(new_filename)

    OR

cv2.imencode('.png', IMAGE)[1].tobytes()
'''

import os.path
import PySimpleGUI as sg
import cv2

def process_and_view_image():
    '''Process and display the image.'''
    try:
        file_name = os.path.join(
            VALUES["-FOLDER-"], VALUES["-FILE LIST-"][0]
        )
        WINDOW["-IMAGE_FILE-"].update(file_name)
        image = cv2.imread(file_name) # pylint: disable=no-member

        # Resize the image if the dimension is to large.
        if image.shape[0] > 999 and image.shape[1] > 768:
            image = cv2.resize(image, (1024, 768), interpolation=cv2.INTER_NEAREST) # pylint: disable=no-member

        WINDOW["-IMAGE-"].update(data=cv2.imencode('.png', image)[1].tobytes()) # pylint: disable=no-member
        # WINDOW["-IMAGE-"].update(filename=FILENAME)
        WINDOW["-STATIC_TEXT-"].update("Image Selected:", font=("Helvetica", 12))

    except: # pylint: disable=bare-except
        pass

def up_down_arrow_key_selection(arrow_key_event):
    '''Process the list selection usingt he Up and Down arrow key events.
    More information related to up/down arrow key seletion on a listbox
    can be viewed @ https://github.com/PySimpleGUI/PySimpleGUI/issues/1629'''

    try:
        current_index = WINDOW.Element('-FILE LIST-').Widget.curselection()

        if arrow_key_event == 'Up:38':
            current_index = (current_index[0] - 1) % WINDOW.Element('-FILE LIST-').Widget.size()
        elif arrow_key_event == 'Down:40':
            current_index = (current_index[0] + 1) % WINDOW.Element('-FILE LIST-').Widget.size()

        WINDOW.Element('-FILE LIST-').Update(set_to_index=current_index)
        WINDOW.Element('-FILE LIST-').Update(scroll_to_index=current_index)
        WINDOW.write_event_value('-FILE LIST-',
                                 [WINDOW.Element('-FILE LIST-').GetListValues()[current_index]])
    except: # pylint: disable=bare-except
        pass

sg.theme('dark grey 9')

FILE_SELECT_COLUMN_LAYOUT = [
    [sg.Text("Image Folder:")],
    [sg.In(size=(73, 1), enable_events=True, key="-FOLDER-",
           readonly=True, disabled_readonly_background_color='#40444B'),
     sg.FolderBrowse(tooltip="Select a folder", key='-FOLDER_BROWSE-'),],
    [sg.Text("Images Retrieved:")],
    [sg.Listbox(values=[], enable_events=True, size=(80, 45),
                key="-FILE LIST-", bind_return_key=True)],
    [sg.Button("Reset", key="-RESET-"), sg.Button("Exit", key="-Exit-")],]

IMAGE_VIEWER_COLUMN_LAYOUT = [
    [sg.Text("                             Select an image from list", key="-STATIC_TEXT-",
             font=("Helvetica", 25))],
    [sg.Text(size=(110, 1), key="-IMAGE_FILE-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full Window Layout -----
WINDOW_LAYOUT = [[sg.Column(FILE_SELECT_COLUMN_LAYOUT, key='-COL1-'),
                  sg.VSeperator(key='-VSEP-'),
                  sg.Column(IMAGE_VIEWER_COLUMN_LAYOUT, key='-COL2-')],]

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
WINDOW = sg.Window("Py Image Viewer", WINDOW_LAYOUT, margins=(0, 0),
                   icon=CURRENT_WORKING_DIRECTORY + "\\img_view.ico",
                   resizable=False, finalize=True, return_keyboard_events=True)

# Run the Event Loop
while True:
    EVENT, VALUES = WINDOW.read()

    # Exit the viewer in the event of close clicked or exit clicked.
    if EVENT in (sg.WIN_CLOSED, "-Exit-"):
        break

    # Restore the window to the initial state on the event of Reset.
    if EVENT == "-RESET-":
        WINDOW["-IMAGE_FILE-"].update('')
        WINDOW["-IMAGE-"].update(filename='')
        WINDOW['-FILE LIST-'].update(values=[])
        WINDOW["-STATIC_TEXT-"].update("                             Select an image from list",
                                       font=("Helvetica", 25))
        WINDOW["-FOLDER-"].update('')

    # Extract the list of image files in the selected folder.
    if EVENT == "-FOLDER-":
        FOLDER = VALUES["-FOLDER-"]
        try:
            # Get list of files in folder
            FILE_LIST = os.listdir(FOLDER)
        except: # pylint: disable=bare-except
            FILE_LIST = []

        FNAMES = [imgfile for imgfile in FILE_LIST
                  if os.path.isfile(os.path.join(FOLDER, imgfile))]

        WINDOW["-FILE LIST-"].update(FNAMES)

    elif EVENT == "-FILE LIST-": # Display the image selected.
        process_and_view_image()

    elif EVENT == 'Up:38':
        up_down_arrow_key_selection(EVENT)
        process_and_view_image()
    elif EVENT == 'Down:40':
        up_down_arrow_key_selection(EVENT)
        process_and_view_image()

WINDOW.close()

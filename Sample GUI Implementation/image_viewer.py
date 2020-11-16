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
'''

import os.path
import PySimpleGUI as sg

FILE_SELECT_COLUMN_LAYOUT = [
    [sg.Text("Image Folder"),
     sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
     sg.FolderBrowse(),],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],]

IMAGE_VIEWER_COLUMN_LAYOUT = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-IMAGE_FILE-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full Window Layout -----
WINDOW_LAYOUT = [[sg.Column(FILE_SELECT_COLUMN_LAYOUT),
                  sg.VSeperator(), sg.Column(IMAGE_VIEWER_COLUMN_LAYOUT),]]

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
WINDOW = sg.Window("Image Viewer", WINDOW_LAYOUT, icon=CURRENT_WORKING_DIRECTORY + "\\img_view.ico")

# Run the Event Loop
while True:
    EVENT, VALUES = WINDOW.read()
    if EVENT in (sg.WIN_CLOSED, "Exit"):
        break
    # Folder name was filled in, make a list of files in the folder
    if EVENT == "-FOLDER-":
        FOLDER = VALUES["-FOLDER-"]
        try:
            # Get list of files in folder
            FILE_LIST = os.listdir(FOLDER)
        except:
            FILE_LIST = []

        FNAMES = [
            imgfile for imgfile in FILE_LIST
            if os.path.isfile(os.path.join(FOLDER, imgfile))
            and imgfile.lower().endswith((".png", ".gif"))
        ]
        WINDOW["-FILE LIST-"].update(FNAMES)
    elif EVENT == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            FILENAME = os.path.join(
                VALUES["-FOLDER-"], VALUES["-FILE LIST-"][0]
            )
            WINDOW["-IMAGE_FILE-"].update(FILENAME)
            WINDOW["-IMAGE-"].update(filename=FILENAME)

        except:
            pass

WINDOW.close()

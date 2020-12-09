"""
    tic-tac-toe Game using PySimpleGUI

    An update to the initial version where once the current board is
    Won/Complete, a Yes/No popup would let the players decide
    if they would want to continue playing.

    YES would let them continue playing the game.
    NO would take the control back to the game
    initialization window to start a fresh session with
    new players.

    Design pattern used for implementing multiple windows
    Using read_all_windows() @
    https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Design_Pattern_Multiple_Windows1.py

    Only 1 window at a time is visible/active on the screen.

    1. INIT_WINDOW opens the GAME_BOARD screen.

    2. Closing the GAME_BOARD exits the game and
    returns to the INIT_WINDOW with the details
    from the previous session intact.

    3. Exiting the INIT_WINDOW would exit the game.

    4. RESET would reset thecurrent game session and
    start over a fresh board.
"""

import os
import numpy as np
import PySimpleGUI as sg

# change the default theme.
# sg.theme('dark grey 9')

INIT_WINDOW = None
GAME_BOARD = None

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
X_IMAGE = CURRENT_WORKING_DIRECTORY + '\\X.png'
X_RED = CURRENT_WORKING_DIRECTORY + '\\X_Red.png'
O_IMAGE = CURRENT_WORKING_DIRECTORY + '\\O.png'
O_RED = CURRENT_WORKING_DIRECTORY + '\\O_Red.png'
GAME_ICON = CURRENT_WORKING_DIRECTORY + '\\tictactoe.ico'

START_GAME: bool = False
CHECK_FOR_WINNER: bool = False
MAIN_DIAGONAL_IS_WINNER: bool = False
CONTINUE_WITH_NEXT_GAME: str = ''
STEP_COUNTER: int = 0
PLAYER_SWITCH = True

PLAYER1_NAME: str = ''
PLAYER1_MARKER: str = ''
PLAYER2_NAME: str = ''
PLAYER2_MARKER: str = ''

ROWS, COLS = (3, 3)
GAME_PROGRESS_ARRAY = [['' for i in range(COLS)] for j in range(ROWS)]
GAME_PROGRESS_ARRAY = np.array(GAME_PROGRESS_ARRAY, dtype=str)
# WINNING_PATTERNS: list = [['00', '10', '20'], ['01', '11', '21'], ['02', '12', '22'], # rows
#                           ['00', '01', '02'], ['10', '11', '12'], ['20', '21', '22'], # columns
#                           ['00', '11', '22'], ['00', '11', '02']] # diagonals

def split(word):
    '''splits a string to constituents chars.'''
    return [int(char) for char in word]

def progress_game(key: str, player_marker: str):
    '''populated the 'GAME_PROGRESS_ARRAY' and
    checks for is winning condition.

    PARAMS:
    1. key - the button element in the grid that was clicked.

    2. player_marker - the marker of the current player.

    RETURNS:
    continue_with_next_game - 'Yes' / 'No' indicator from the user action
    whether to continue with the same players.
    '''

    global GAME_PROGRESS_ARRAY

    continue_with_next_game: str = ''

    row, column = split(key)
    GAME_PROGRESS_ARRAY[row][column] = player_marker

    # check if we have a winner in the current state of the board.
    if CHECK_FOR_WINNER:
        game_won, winning_marker = is_winning()
        if game_won:
            continue_with_next_game = display_winner_and_continue(winning_marker=winning_marker)
        else:
            # GAME DRAWN - GAME_PROGRESS_ARRAY is full and we do not have a winner.
            if np.all((GAME_PROGRESS_ARRAY != '')):
                continue_with_next_game = display_winner_and_continue(winning_marker='')

    return continue_with_next_game

def is_row_column_diagonal_complete(row_col_num: int = -1, is_row: bool = True,
                                    is_diagonal: bool = False):
    '''checks if the given row or column is complete
    to proceed with a winner.

    PARAMS:
    1. row_col_num - the row/column index to check if the row/columns is complete.
    2. is_row: True if a ROW needs to be checked for completion else FALSE for a column.
    3. is_diagonal: True is any of the diagonal needs to be checked for completion.

    RETURNS:
    is_complete: BOOLEAN FLAG to indicate of the row/column/diagonal is complete.
    '''
    is_complete: bool = False

    if is_diagonal is False and row_col_num != -1:
        if is_row:
            row = row_col_num
            is_complete = GAME_PROGRESS_ARRAY[row][0] != '' and \
                          GAME_PROGRESS_ARRAY[row][1] != '' and \
                          GAME_PROGRESS_ARRAY[row][2] != ''
        else:
            col = row_col_num
            is_complete = GAME_PROGRESS_ARRAY[0][col] != '' and \
                          GAME_PROGRESS_ARRAY[1][col] != '' and \
                          GAME_PROGRESS_ARRAY[2][col] != ''
    else:
        if GAME_PROGRESS_ARRAY[0][0] != '' and \
            GAME_PROGRESS_ARRAY[1][1] != '' and \
                GAME_PROGRESS_ARRAY[2][2] != '':
            is_complete = True

        if GAME_PROGRESS_ARRAY[2][0] != '' and \
                GAME_PROGRESS_ARRAY[1][1] != '' and \
                    GAME_PROGRESS_ARRAY[0][2] != '':
            is_complete = True

    return is_complete

def mark_the_winner(row_is_winner: bool, row_column_index: int = -1,
                    diagonal_is_winner: bool = False):
    '''marks the winner row/column by updating
    the button row/column. The button image background
    changes to red to mark the winning sequence.

    PARAMS:
    1. row_is_winner - Is the winner found in a ROW wise sequence.
    TRUE for a row & FALSE incase the winner is a column.

    2. row_column_index - The winning row/column index.
    This default value is -1 to indicate the winner being found
    in one of the diagonals.

    3. diagonal_is_winner - Is the winner found in one of the diagonals.
    '''

    if not diagonal_is_winner and row_column_index != -1:
        if row_is_winner:
            row = row_column_index
            if GAME_PROGRESS_ARRAY[row][0] == 'X':
                GAME_BOARD.Element(str(row)+str(0)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(row)+str(1)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(row)+str(2)).update(image_filename=X_RED)
            else:
                GAME_BOARD.Element(str(row)+str(0)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(row)+str(1)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(row)+str(2)).update(image_filename=O_RED)
        else:
            col = row_column_index
            if GAME_PROGRESS_ARRAY[0][col] == 'X':
                GAME_BOARD.Element(str(0)+str(col)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(1)+str(col)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(2)+str(col)).update(image_filename=X_RED)
            else:
                GAME_BOARD.Element(str(0)+str(col)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(1)+str(col)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(2)+str(col)).update(image_filename=O_RED)
    else:
        if MAIN_DIAGONAL_IS_WINNER:
            if GAME_PROGRESS_ARRAY[1][1] == 'X':
                GAME_BOARD.Element(str(0)+str(0)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(2)+str(2)).update(image_filename=X_RED)
            else:
                GAME_BOARD.Element(str(0)+str(0)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(2)+str(2)).update(image_filename=O_RED)
        else:
            if GAME_PROGRESS_ARRAY[1][1] == 'X':
                GAME_BOARD.Element(str(0)+str(2)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=X_RED)
                GAME_BOARD.Element(str(2)+str(0)).update(image_filename=X_RED)
            else:
                GAME_BOARD.Element(str(0)+str(2)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=O_RED)
                GAME_BOARD.Element(str(2)+str(0)).update(image_filename=O_RED)

def is_winning():
    '''evaluated the current state of the gameboard
    and checks if there is a winner currently.'''

    global GAME_PROGRESS_ARRAY
    global CHECK_FOR_WINNER
    global MAIN_DIAGONAL_IS_WINNER

    # check for the row wise sequence.
    for row in range(ROWS):
        if is_row_column_diagonal_complete(row_col_num=row, is_row=True):
            if GAME_PROGRESS_ARRAY[row][0] == GAME_PROGRESS_ARRAY[row][1] == GAME_PROGRESS_ARRAY[row][2]:
                mark_the_winner(row_is_winner=True, row_column_index=row)
                CHECK_FOR_WINNER = False
                return True, GAME_PROGRESS_ARRAY[row][0]

    # check for the column wise sequence.
    for col in range(COLS):
        if is_row_column_diagonal_complete(row_col_num=col, is_row=False):
            if GAME_PROGRESS_ARRAY[0][col] == GAME_PROGRESS_ARRAY[1][col] == GAME_PROGRESS_ARRAY[2][col]:
                mark_the_winner(row_is_winner=False, row_column_index=col)
                CHECK_FOR_WINNER = False
                return True, GAME_PROGRESS_ARRAY[0][col]

    # check for the 2 diagonals for a winning sequence.
    if is_row_column_diagonal_complete(is_diagonal=True):
        if GAME_PROGRESS_ARRAY[0][0] == GAME_PROGRESS_ARRAY[1][1] == GAME_PROGRESS_ARRAY[2][2]:
            MAIN_DIAGONAL_IS_WINNER = True
            mark_the_winner(row_column_index=-1, row_is_winner=False, diagonal_is_winner=True)
            CHECK_FOR_WINNER = False
            return True, GAME_PROGRESS_ARRAY[1][1]

        elif GAME_PROGRESS_ARRAY[2][0] == GAME_PROGRESS_ARRAY[1][1] == GAME_PROGRESS_ARRAY[0][2]:
            mark_the_winner(row_column_index=-1, row_is_winner=False, diagonal_is_winner=True)
            CHECK_FOR_WINNER = False
            return True, GAME_PROGRESS_ARRAY[1][1]

    return False, ''

def display_winner_and_continue(winning_marker: str):
    '''display the winner of the current board.

    PARAMS:
    1. winning_marker - the marker that won the current board.
    '''

    if winning_marker == PLAYER1_MARKER:
        popup_result = sg.PopupYesNo('The Winner is ' + PLAYER1_NAME + '.\nDo you want to play another game with the current players?',
                                     title='Board Winner!', text_color='darkblue', icon=GAME_ICON, grab_anywhere=True)
    elif winning_marker == PLAYER2_MARKER:
        popup_result = sg.PopupYesNo('The Winner is ' + PLAYER2_NAME + '.\nDo you want to play another game with the current players?',
                                     title='Board Winner!', text_color='darkblue', icon=GAME_ICON, grab_anywhere=True)
    else: # game drawn
        popup_result = sg.PopupYesNo('The Game is DRAWN.\nDo you want to play another game with the current players?',
                                     title='Board Drawn!', text_color='darkblue', icon=GAME_ICON, grab_anywhere=True)

    return popup_result

def init_game_window():
    '''Initializes and creates the game options window.'''

    init_game_layout = [[sg.Text('Player 1 Name: ', size=(12, 1)),
                         sg.InputText('', key='-P1_NAME-')],
                        [sg.Text('Player 2 Name: ', size=(12, 1)),
                         sg.InputText('', key='-P2_NAME-')],
                        [sg.Frame(layout=[[sg.Radio('X', group_id="P1_PREF", key='-P1_MARK-',
                                                    default=True, size=(10, 1)),
                                           sg.Radio('O', group_id="P1_PREF", key='-P2_MARK-')]],
                                  title='Player 1 Preference', relief=sg.RELIEF_GROOVE,
                                  tooltip='Set Player 1 Preference')],
                        [sg.Button("Start Game", key='-START-'), sg.Button('Exit', key='-EXIT-')]]

    return sg.Window('Tic Tac Toe Options', init_game_layout, icon=GAME_ICON, finalize=True)

def reset_game_board(reset_board: str):
    '''Resets the current game board and re-initializes all the
    game parameters to continue playing the game with the same players.
    
    PARAMS:
    1. reset_board - resets the current board to the initial state.
    '''

    global GAME_PROGRESS_ARRAY
    global STEP_COUNTER
    global CONTINUE_WITH_NEXT_GAME
    global CHECK_FOR_WINNER
    global GAME_BOARD
    global PLAYER_SWITCH
    global MAIN_DIAGONAL_IS_WINNER

    if reset_board == 'Yes':
        GAME_BOARD = initialize_game_board()

    GAME_PROGRESS_ARRAY = [['' for i in range(COLS)] for j in range(ROWS)]
    GAME_PROGRESS_ARRAY = np.array(GAME_PROGRESS_ARRAY, dtype=str)
    STEP_COUNTER = 0
    CHECK_FOR_WINNER = False
    CONTINUE_WITH_NEXT_GAME = ''
    PLAYER_SWITCH = True
    MAIN_DIAGONAL_IS_WINNER = False

def start_next_session(user_choice: str):

    '''starts the next session as per the user choice.
    YES - retain the players and reset the board state.
    NO - return to the game init dialog to start over with new set of players.'''

    global INIT_WINDOW
    global GAME_BOARD

    if user_choice == 'Yes':
        # retain the players and reset the board state.
        GAME_BOARD.Close()
        GAME_BOARD = None
        reset_game_board(reset_board='Yes')
    elif user_choice == 'No':
        # return to the game init dialog to start over with new set of players.
        GAME_BOARD.Close()
        GAME_BOARD = None
        reset_game_board(reset_board='No')
        INIT_WINDOW = init_game_window()

def initialize_game_board():
    '''initialize the game board.'''

    global PLAYER1_NAME
    global PLAYER1_NAME
    global PLAYER1_MARKER
    global PLAYER2_MARKER

    GAME_BOARD_LAYOUT = [[sg.Text('Player 1: ' + PLAYER1_NAME, key='-P1-', text_color='darkblue')],
                        [sg.Text('Player 2: ' + PLAYER2_NAME, key='-P2-', text_color='white')],
                        [sg.Text(PLAYER1_NAME + "'s Marker: " + PLAYER1_MARKER)],
                        [sg.Text(PLAYER2_NAME + "'s Marker: " + PLAYER2_MARKER)],
                        [sg.Text('')]]

    GAME_BOARD_LAYOUT += [[sg.Button(' ', size=(8, 4), key=str(j)+str(i))
                            for i in range(3)] for j in range(3)]

    GAME_BOARD_LAYOUT += [[sg.Button("Reset Game", key="-RESET-", tooltip='Resets the current session.')]]

    BOARD = sg.Window('Tic Tac Toe', GAME_BOARD_LAYOUT, icon=GAME_ICON, finalize=True)

    BOARD.TKroot.protocol("WM_DESTROY_WINDOW", lambda: BOARD.write_event_value("WIN_CLOSE", ()))
    BOARD.TKroot.protocol("WM_DELETE_WINDOW", lambda: BOARD.write_event_value("WIN_CLOSE", ()))

    return BOARD

# Design pattern 1 - First window does not remain active
GAME_BOARD = None
INIT_WINDOW = init_game_window()

while True:

    WINDOW, EVENT, VALUES = sg.read_all_windows()

    if EVENT in (sg.WIN_CLOSED, '-EXIT-') and WINDOW == INIT_WINDOW:
        break

    if EVENT == '-START-' and not GAME_BOARD:

        # player name validation. Valid names required.
        if VALUES['-P1_NAME-'] == '' and VALUES['-P2_NAME-'] == '':
            sg.popup_ok("Error initializing players name. Enter both the players name before proceeding.",
                        title='Tic Tac Toe', icon=GAME_ICON)

        else:
            PLAYER1_NAME, PLAYER2_NAME, PLAYER1_X, PLAYER2_X = VALUES['-P1_NAME-'], VALUES['-P2_NAME-'], VALUES['-P1_MARK-'], VALUES['-P2_MARK-']

            # Get the PLayer Markers to start with.
            if PLAYER1_X:
                PLAYER1_MARKER, PLAYER2_MARKER = ("X", "O")
            else:
                PLAYER1_MARKER, PLAYER2_MARKER = ("O", "X")

            # set the flag to start the game as once the
            # window is closed the event loop will be destroyed.
            if EVENT == '-START-':
                if VALUES['-P1_NAME-'] is not None and VALUES['-P2_NAME-'] is not None:
                    START_GAME = True
                    # Close the options window and start the game.
                    INIT_WINDOW.close()
                    GAME_BOARD = initialize_game_board()

    if WINDOW == GAME_BOARD and (EVENT in ('WIN_CLOSE', '-EXIT-')):
        GAME_BOARD.close()
        GAME_BOARD = None
        INIT_WINDOW = init_game_window()

    # We do not want to execute the progress logic in case
    # of the reset event.
    if START_GAME and EVENT != '-RESET-':

        if EVENT not in ('-START-', 'WIN_CLOSE', '-EXIT-'):

            CURRENT_MARKER = GAME_BOARD.Element(EVENT).get_text()
            GAME_BOARD.Element(EVENT).update(PLAYER1_MARKER if CURRENT_MARKER == ' ' and\
                                             PLAYER_SWITCH is True else PLAYER2_MARKER if CURRENT_MARKER == ' ' and\
                                             PLAYER_SWITCH is False else PLAYER1_MARKER if CURRENT_MARKER == PLAYER1_MARKER
                                             else PLAYER2_MARKER if CURRENT_MARKER == PLAYER2_MARKER else ' ')

            # Change the color of the player text to mark
            # the next player's turn. 'DarkBlue' indicates
            # the player who should make the next move.'
            # Additionally, Once the player has made a move,
            # disable the button.
            if GAME_BOARD.Element(EVENT).get_text() == PLAYER1_MARKER:
                # increase the step counter.
                # The minimum number of steps required to win the game is 5
                STEP_COUNTER += 1
                PLAYER_SWITCH = False

                GAME_BOARD.Element('-P1-').update(text_color='white')
                GAME_BOARD.Element('-P2-').update(text_color='darkblue')

                # update the button images as per the current players marker.
                if PLAYER1_MARKER == 'X':
                    GAME_BOARD.Element(EVENT).update(image_filename=X_IMAGE)
                else:
                    GAME_BOARD.Element(EVENT).update(image_filename=O_IMAGE)

                GAME_BOARD.Element(EVENT).update(disabled=True)

                CONTINUE_WITH_NEXT_GAME = progress_game(EVENT, PLAYER1_MARKER)

                # start with the same players or new game
                # session with different players
                start_next_session(CONTINUE_WITH_NEXT_GAME)

            elif GAME_BOARD.Element(EVENT).get_text() == PLAYER2_MARKER:
                # increase the step counter.
                # The minimum number of steps required to win the game is 5
                STEP_COUNTER += 1
                PLAYER_SWITCH = True

                GAME_BOARD.Element('-P1-').update(text_color='darkblue')
                GAME_BOARD.Element('-P2-').update(text_color='white')

                # update the button images as per the current players marker.
                if PLAYER2_MARKER == 'X':
                    GAME_BOARD.Element(EVENT).update(image_filename=X_IMAGE)
                else:
                    GAME_BOARD.Element(EVENT).update(image_filename=O_IMAGE)

                GAME_BOARD.Element(EVENT).update(disabled=True)

                CONTINUE_WITH_NEXT_GAME = progress_game(EVENT, PLAYER2_MARKER)

                # start with the same players or new game
                # session with different players
                start_next_session(CONTINUE_WITH_NEXT_GAME)

            # The minimum number of steps required
            # to win the game board is 5.
            if STEP_COUNTER == 4:
                CHECK_FOR_WINNER = True

    if EVENT == '-RESET-' and WINDOW == GAME_BOARD:
        # reset the current board state.
        RESET_GAME = sg.popup_yes_no('Are you sure you want to reset the current board?',
                                     title='Game Reset', icon=GAME_ICON, grab_anywhere=True)
        if RESET_GAME == 'Yes':
            GAME_BOARD.Close()
            GAME_BOARD = None
            reset_game_board(reset_board='Yes')

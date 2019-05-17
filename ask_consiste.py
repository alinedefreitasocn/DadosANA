# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:32:33 2019

@author: aline
"""

import PySimpleGUI as sg

# This design pattern simulates button callbacks
# Note that callbacks are NOT a part of the package's interface to the
# caller intentionally.  The underlying implementation actually does use
# tkinter callbacks.  They are simply hidden from the user.

# The callback functions

    # Layout the design of the GUI
def ask():
    layout = [[sg.Text('   Selecione o nivel de consistencia dos dados', auto_size_text=True)],
              [sg.Text('              '), sg.Button('Brutos'), sg.Button('Consistidos'), ]]

    # Show the Window to the user
    window = sg.Window('Button callback example', layout)

    # Event loop. Read buttons, make callbacks
    #while True:
        # Read the Window
    event, value = window.Read()
    # Take appropriate action based on button
    if event == 'Brutos':
        nconsiste = 1
        window.Close()
    elif event == 'Consistidos':
        nconsiste = 2
    return nconsiste

# All done!
#sg.PopupOK('Done')
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:14:06 2019

@author: aline
"""

import pandas as pd
import PySimpleGUI as sg
import datetime as dt
import os
import glob


from ano_hidrologico import ano_hidrologico
from reescrevendo_ANA import reescreve
from ask_consiste import ask
from find_nth import find_nth

path = sg.PopupGetFolder('Pasta com arquivos da ANA a serem trabalhados')

" ************************************************************************** "
"                                                                            "
"                 1.  REESCREVER OS ARQUIVOS DA ANA                          "
"                                                                            "
" ************************************************************************** "


listfiles = glob.glob(path + '/*.csv', recursive=True)

nconsiste = ask()

current_value = 0
for file in listfiles:
    current_value += 1
    max_value = len(listfiles)
    w = sg.OneLineProgressMeter('Reescrevendo...', current_value, max_value, 'key')
    reescreve(file, nconsiste)
    current_value += 1


" ************************************************************************** "
"                                                                            "
"                 2. GERAR TABELAS COM OS MAXIMOS                            "
"                                                                            "
" ************************************************************************** "
listfiles_reescritos = glob.glob(path + '/*_serie_temporal.csv',
                                 recursive=True)

for arquivo in listfiles_reescritos:
    df = pd.read_csv(arquivo,
                     sep=';',
                     header=0,
                     thousands=',',
                     index_col='datahora',
                     parse_dates=True
                     )
    df.chuva = df.chuva/10
    name = arquivo[find_nth(arquivo, '_', 2)+1 : find_nth(arquivo, '_', 3)]
    ano_hidrologico(df, name, path)


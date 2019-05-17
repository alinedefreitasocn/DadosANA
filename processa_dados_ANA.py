# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:14:06 2019

@author: aline

Em breve será um script de processamento total dos dados da ANA
Até agora (17/05/2018) consegue:
    1. Reescrever os arquivos da ANA: passar do formato original de tabela para
    o formato de série temporal com a opção de escolher usar os dados brutos ou
    os consistidos pela própria ANA (ask_consiste.ask). Gera arquivos CSV com
    nome "serie_temporal" com apenas duas colunas, data e volume de chuva.

    2. Gerar as tabelas de máximos valores mensais, fornecendo como saida um
    arquivo em csv com colunas de ano inicial e final, o valor maximo de chuva
    e a data de ocorrencia do evento. Utiliza o padrão de ano hidrologico indo
    de 01/10/ano ate 30/09/ano+1
        adiciona um limite de 350 registros dentro do ano hidrologico para
        determinar o valor maximo de pluviosidade.
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

path = sg.PopupGetFolder('Pasta com arquivos a serem trabalhados')

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
    w = sg.OneLineProgressMeter('Reescrevendo...',
                                current_value,
                                max_value,
                                'key')
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


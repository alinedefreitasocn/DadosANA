# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 10:05:09 2019

@author: Aline Lemos de Freitas
@date: 2019-04-09



ROTINA PARA LER O ARQUIVO DA ANA REESCREVENDO PARA UM SERIE TEMPORAL
COM OS REGISTROS DIARIOS DE CHUVA

PODEMOS DEPOIS TRANSFORMAR ISSO NUMA FUNCAO


ATENCAO!! ESTA PULANDO OS DIAS 29 DE FEVEREIRO PARA ANOS BISSEXTOS. ISSO
AINDA PRECISA SER AJUSTADO, MAS NAO SEI MUITO BEM COMO.



"""

import pandas as pd
import numpy as np
import PySimpleGUI as sg
import os

" ALTERAR SOMENTE ESSA LINHA COM O PATHNAME E O NOME DO ARQUIVO A SER LIDO "
" SEPARADOS POR VIRGULA E COM A ULTIMA CONTRABARRA NA VARIAVEL DO FILENAME "
def ano_bissexto(ano):
    if ano % 4 == 0:
        if ano % 100 != 0:
            if ano % 400 == 0:
                return True
    return False

def reescreve(file, nconsiste):
#    file = sg.PopupGetFile('Arquivo ANA original')
    path, filename = os.path.split(file)
    "Lendo arquivo da ANA"
    ANA = pd.read_csv(file,
                      sep=';',
                      header=0,
                      na_values='',
                      dayfirst=True,
                      skiprows=12,
                      parse_dates=[2],
                      index_col=2)

    # Dados da ANA estavam com entradas duplicadas...Uma linha eh dado
    # consistido e o outro eh bruto. Selecionar as linhas dos brutos
    # pq tem meses faltando nos consistidos.
    # Daddos foram consistidos ate 2006-10-01
    # Selecionando apenas os valores consistidos, quando existentes
    # Nive consistencia == 1 == Dado Bruto
    # Nivel consistencia == 2 == Consistido

    " funcao ask() so abre um GUI perguntando se deseja usar"
    " os dados brutos ou consistidos "

    ANA_consist = ANA[ANA.NivelConsistencia == nconsiste]
    # completando com os dados brutos nos registros onde nao houve
    # consistencia
    #ANA_bruto = ANA[ANA.index > '2006-10-01']
    #ANA = ANA_consist.append(ANA_bruto)


    " Cria uma nova variavel soh com as colunas de chuva diaria "
    "                chamada chuva_diaria                       "
    #Contruindo uma lista de nome das colunas de chuva
    list_nome_col = []
    for i in np.arange(1, 32):
        if i < 10:
            nome_col = ('Chuva' + '0' + str(i))
        else:
            nome_col = ('Chuva' + str(i))
        list_nome_col.append(nome_col)

    chuva_diaria = ANA_consist[list_nome_col].copy()
    #chuva_diaria = chuva_diaria[chuva_diaria > 0.2]
    #
    #chuva_diaria_media = np.array(chuva_diaria.groupby(
    #        by=chuva_diaria.index.month).mean())

    ANA_serie_temporal = pd.DataFrame(columns=['datahora', 'chuva'])
    " Le linha por linha atraves das colunas de dia "
    #diasdechuva = []
    for line in chuva_diaria.index:
    #    b = [0]      # sempre zerar
    #    chuva = []  # sempre zerar
        " { Pega a linha toda a partir do indice de data} "
    #    chuva = chuva_diaria[chuva_diaria.index == line]
        " { Percorre cada uma das colunas } "
        for header in list_nome_col:
    #        dia = int(header[-2:])  # pega so o numero do dia. i eh o nome da col
    #        mes = line.month
    #        ano = line.year

            if int(header[-2:]) == 31 and line.month in [4, 6, 9, 11]:
                continue

            elif line.month == 2 and int(header[-2:]) in range(29, 32) and not(bissexto):
                continue

            elif line.month == 2 and int(header[-2:]) in range(30, 32) and bissexto:
                continue

            datahora = pd.Timestamp(line.year, line.month, int(header[-2:]))
            valor_chuva = chuva_diaria[chuva_diaria.index == line][header][0]
            ANA_serie_temporal = ANA_serie_temporal.append({'datahora':datahora,
                                                            'chuva':valor_chuva},
                                                            ignore_index=True)

    ANA_serie_temporal.index = ANA_serie_temporal.datahora
    ANA_serie_temporal = ANA_serie_temporal.drop('datahora', axis=1)

    ANA_serie_temporal.to_csv(path + '/' + filename[:-4] + '_serie_temporal.csv',
                              sep=';',
                              na_rep='NaN')
    #        if chuva[i][0] > lim_chuva:
    #            a = int(b[ii-1]) + 1
    #            b.insert(ii, a)
    #        else:
    #            b.insert(ii, 0)
    #    b = np.array(b)
    #    diasdechuva.append(b)
    #diasdechuva=pd.DataFrame(diasdechuva, index=datahora)


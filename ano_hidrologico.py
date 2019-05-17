# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:58:59 2019
@author: bx22
SELECIONANDO ANO HIDROLOGICO
"""

import pandas as pd
import datetime as dt
from find_nth import find_nth
import numpy as np


def ano_hidrologico(df, name, path):
    anos = pd.unique(df.index.year)
    anoss = np.sort(anos)

    # como ele eh conjunto aberto, nao inclui os valores mostrados
    maximos_mensais = pd.DataFrame(columns = ['Ano Inicio', 'Ano Fim', 'Data', 'Maximo'])
    for ano in anoss:
        water_year = []
        data_inicio = dt.datetime(ano, 9, 30)
        data_fim = dt.datetime(ano + 1, 10, 1)
        water_year = df[ (df.index > data_inicio) & (df.index < data_fim) ]
        if len(water_year) < 350:
            maximo_data = np.NAN
            maximo_valor = np.NAN
        else:
            maximo_data = str(water_year.index[water_year.chuva == water_year.chuva.max()])
            maximo_data = maximo_data[find_nth(maximo_data, '[', 1)+2:find_nth(maximo_data, ']', 1)-1]
            maximo_valor = water_year.chuva.max()
        maximos_mensais = maximos_mensais.append({'Data': maximo_data,
                                                  'Maximo': "{:10.2f}".format(maximo_valor),
                                                  'Ano Inicio': ano,
                                                  'Ano Fim' : ano+1},
                                                    ignore_index=True)

    maximos_mensais.to_csv(path + '/' + name + '_maximos_mensais.csv', sep=';')
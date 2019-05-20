# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:58:59 2019
@author: bx22
SELECIONANDO ANO HIDROLOGICO

A divisão por ano hidrológico considera o período de 01/10 de um ano até
30/09 do ano seguinte. Assim, é necessário dividir a série temporal em
blocos manualmente para fazer as devidas análises.

Esse caso expecifio foi desenvolvido para o calculo dos máximos anuais
de chuva nas estações pluviometricas da ANA de acordo com o ano hidrologico.

"""

import pandas as pd
import datetime as dt
from find_nth import find_nth
import numpy as np


def ano_hidrologico(df, name, path):
    # pega os anos no idice com dataFrame e determina os valores 
    # nao repetidos
    anos = pd.unique(df.index.year)
    # coloca em ordem pq tava dando erro na hora de montar a tabela
    anoss = np.sort(anos)
    
    # cria a estrutura da minha tabela de saida
    maximos_anuais = pd.DataFrame(columns = ['Ano Inicio', 'Ano Fim', 'Data', 'Maximo'])
    
    for ano in anoss:
        water_year = []
        # como eh conjunto aberto, nao inclui os valores mostrados
        data_inicio = dt.datetime(ano, 9, 30)
        data_fim = dt.datetime(ano + 1, 10, 1)
        # seleciona so as ocorrencias dentro daquele ano hidrologico
        water_year = df[ (df.index > data_inicio) & (df.index < data_fim) ]
        # valor de 350 estipulado para evitar que ele calcule os maximos
        # quando tiver um ano incompleto (ex., ano inicial e final da serie)
        # ou quando houver muitas falhas nos dados
        if len(water_year) < 350:
            maximo_data = np.NAN
            maximo_valor = np.NAN
        else:
            maximo_data = str(water_year.index[water_year.chuva == water_year.chuva.max()])
            # udando o find_nth para pegar so o valor da data. como ele tá num formato de 
            # datetime, tava entrando com esse formato na tabela e tava ficando enorme
            maximo_data = maximo_data[find_nth(maximo_data, '[', 1)+2:find_nth(maximo_data, ']', 1)-1]
            maximo_valor = water_year.chuva.max()
        # criando a tabela de saida com os valores encontrados para cada ano
        maximos_anuais = maximos_anuais.append({'Data': maximo_data,
                                                  'Maximo': "{:10.2f}".format(maximo_valor),
                                                  'Ano Inicio': ano,
                                                  'Ano Fim' : ano+1},
                                                   ignore_index=True)

    maximos_anuais.to_csv(path + '/' + name + '_maximos_anuais.csv', sep=';')

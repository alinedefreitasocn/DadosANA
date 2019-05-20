# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 10:05:09 2019

@author: Aline Lemos de Freitas
@date: 2019-04-09


ROTINA PARA LER O ARQUIVO DA ANA REESCREVENDO PARA UM SERIE TEMPORAL
COM OS REGISTROS DIARIOS DE CHUVA

MICHEL RESOLVEU A QUESTAO DO ANO BISSEXTO CRIANDO A FUNCAO ANO_BISSEXTO

AGORA EH UMA FUNCAO QUE TEM COMO ENTRADA O NOME DO ARQUIVO E O 
NCONSISTE, QUE EH O VALOR DE SAIDA DA FUNCAO ASK_CONSISTE
DIZENDO SE VAI PEGAR OS DADOS CONSISTIDOS OU OS BRUTOS
DA SERIE DA ANA



"""

import pandas as pd
import numpy as np
import PySimpleGUI as sg
import os


def ano_bissexto(ano):
    if ano % 4 == 0:
        if ano % 100 != 0:
            if ano % 400 == 0:
                return True
    return False

def reescreve(file, nconsiste):
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
    
    # Contruindo uma lista de nome das colunas de chuva
    list_nome_col = []
    # AS COLUNAS DO ARQUIVO SAO NOMEADAS COMO CHUVA+DIA
    # ONDE DIA VARIA DE 1 A 31
    # pequeno loop para do caso dos dias menores que 10
    # adiciona um zero a esquerda
    for i in np.arange(1, 32):
        if i < 10:
            nome_col = ('Chuva' + '0' + str(i))
        else:
            nome_col = ('Chuva' + str(i))
        list_nome_col.append(nome_col)
    
    # seleciona so as colunas que apresentam os valores de chuva
    # descartando as demais. copia para um novo df
    chuva_diaria = ANA_consist[list_nome_col].copy()
    
    ANA_serie_temporal = pd.DataFrame(columns=['datahora', 'chuva'])
    
    # percorre cada uma das linhas do arquivo atraves do indice
    # depois percorre cada uma das colunas naquela linha
    # pegando assim o valor do acumulado para aquele dia
    # e depois montando um novo datetime a partir da combinacao
    # linha indice vs coluna header
    " { Pega a linha toda a partir do indice de data} "
    for line in chuva_diaria.index:
        " { Percorre cada uma das colunas } "
        for header in list_nome_col:
    #        dia = int(header[-2:])  # pega so o numero do dia. i eh o nome da col
    #        mes = line.month
    #        ano = line.year
            # faz uns testes para evitar que ele tente pegar o valor do dia 31
            # de um mes que vai soh ate 30 e solucionando o problema do ano
            # bissexto nos meses de fevereiro
            if int(header[-2:]) == 31 and line.month in [4, 6, 9, 11]:
                continue
            elif line.month == 2 and int(header[-2:]) in range(29, 32) and not(bissexto):
                continue
            elif line.month == 2 and int(header[-2:]) in range(30, 32) and bissexto:
                continue
            
            # criando o novo datetime com a compinacao da linha e do header
            datahora = pd.Timestamp(line.year, line.month, int(header[-2:]))
            # pegando o valor acumulado de chuva praquele dia
            valor_chuva = chuva_diaria[chuva_diaria.index == line][header][0]
            ANA_serie_temporal = ANA_serie_temporal.append({'datahora':datahora,
                                                            'chuva':valor_chuva},
                                                            ignore_index=True)

    ANA_serie_temporal.index = ANA_serie_temporal.datahora
    ANA_serie_temporal = ANA_serie_temporal.drop('datahora', axis=1)

    ANA_serie_temporal.to_csv(path + '/' + filename[:-4] + '_' + str(nconsiste) + '_serie_temporal.csv',
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


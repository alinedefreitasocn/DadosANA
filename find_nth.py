# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:16:53 2019
@author: bx22
CRIANDO UMA FUNCAO FIND_NTH QUE PROCURA A NESIMA OCORRENCIA DO CARACTERE
"""
# como rodar!
#def find_nth(string, caracter, occur):
#    location = -1
#    for i in range(occur):
#        location = string.find(caracter, location+1)
#    return location
#
#inicio = find_nth(filename, '_', 1)
#
#fim = find_nth(filename, '_', 3)
#
#titulo = txt[inicio:fim]


def find_nth(string, caracter, occur):
    location = -1
    for i in range(occur):
        location = string.find(caracter, location+1)
    return location
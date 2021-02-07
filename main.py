#!/usr/bin/python3
# -*- coding: utf-8 -*-

from leitor import construir_automato
from conversor import converter_af_para_er

'''
Módulo principal, que utiliza dos outros dois módulos para
ler o AF e convertê-lo para uma expressão regular
'''

grafo, estados = construir_automato()
resposta = converter_af_para_er(grafo, estados)

# Imprime a ER obtida
print(resposta)
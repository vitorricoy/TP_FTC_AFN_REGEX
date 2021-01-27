#!/usr/bin/python3

import numpy as np
import sys

def precisaDeParentesesParaConcatenar(atual):
  fim = atual.find(')')
  if fim == -1:
    return '+' in atual
  
  inicio = atual[:fim].rfind('(')
  while inicio != -1 and fim != -1:
    atual = atual[:inicio] + atual[fim+1:]
    if fim == -1:
      break
    inicio = atual[:fim].rfind('(')
  return '+' in atual

def parentesesNasPontas(resposta):
  posicoesAberto = []
  ultimoRemovido = -1
  for i in range(0, len(resposta)):
    if resposta[i] == '(':
      posicoesAberto.append(i)
    if resposta[i] == ')':
      ultimoRemovido = posicoesAberto.pop()
  return ultimoRemovido == 0 and resposta.endswith(')')

arq = open(sys.argv[1])

estados_string = arq.readline().strip()
estados = estados_string.split(',')
estados.append('estado_inicio_unico')
estados.append('estado_fim_unico')

simbolos_string = arq.readline().strip()
simbolos = simbolos_string.split(',')

estados_iniciais_string = arq.readline().strip()
estados_iniciais = estados_iniciais_string.split(',')

estados_finais_string = arq.readline().strip()
estados_finais = estados_finais_string.split(',')

grafo = {}

for estado1 in estados:
  grafo[estado1] = {}
  for estado2 in estados:
    grafo[estado1][estado2] = ''

for estado in estados_iniciais:
  grafo['estado_inicio_unico'][estado] = 'lambda'

for estado in estados_finais:
  grafo[estado]['estado_fim_unico'] = 'lambda'

for linha in arq:
  lista = linha.strip().split(',')
  for el in lista[2:]:
    if grafo[lista[0]][el]:
      grafo[lista[0]][el]+=' + ' + lista[1]
    else: 
      grafo[lista[0]][el]=lista[1]

# for i in grafo:
#   for j in grafo[i]:
#     print('grafo['+i+']['+j+'] = '+grafo[i][j])

removidos = set()

# Remove os estados
for estado in estados[:-2]:
  selfLoop = False
  if grafo[estado][estado]:
    selfLoop = True
  for estadoEntrada in estados:
    if grafo[estadoEntrada][estado] and estado != estadoEntrada and estadoEntrada not in removidos:
      for estadoSaida in estados:
        if grafo[estado][estadoSaida] and estado != estadoSaida and estadoSaida not in removidos:
          novaAresta = ''
          if grafo[estadoEntrada][estado] != 'lambda':
            if precisaDeParentesesParaConcatenar(grafo[estadoEntrada][estado]):
              novaAresta = '('+grafo[estadoEntrada][estado]+')'
            else:
              novaAresta = grafo[estadoEntrada][estado]
          if selfLoop:
              novaAresta += '('+grafo[estado][estado]+')*'
          if grafo[estado][estadoSaida]!= 'lambda':
            if precisaDeParentesesParaConcatenar(grafo[estado][estadoSaida]):
              novaAresta += '('+grafo[estado][estadoSaida]+')'
            else:
              novaAresta += grafo[estado][estadoSaida]
          if novaAresta == '':
            novaAresta = 'lambda'
          if grafo[estadoEntrada][estadoSaida]:
            grafo[estadoEntrada][estadoSaida]+= ' + '+novaAresta
          else:
            grafo[estadoEntrada][estadoSaida] = novaAresta
          #print('aresta de', estadoEntrada, ' até ', estadoSaida, ' colocou ', novaAresta, ' virou ', grafo[estadoEntrada][estadoSaida])
  for estado2 in estados:
    grafo[estado2][estado] = ''
    grafo[estado][estado2] = ''
  grafo[estado][estado] = ''
  removidos.add(estado)

resposta = grafo['estado_inicio_unico']['estado_fim_unico']
while parentesesNasPontas(resposta):
  resposta = resposta[1:-1]
print(resposta)

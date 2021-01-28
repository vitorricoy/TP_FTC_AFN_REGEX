#!/usr/bin/python3

import numpy as np
import sys

ESTADO_INICIO = 'estado_inicio_unico'
ESTADO_FIM = 'estado_fim_unico'
LAMBDA = 'lambda'

def precisa_parenteses_para_concatenar(atual):
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

def tem_parenteses_nas_pontas(resposta):
    posicoesAberto = []
    ultimoRemovido = -1
    for i in range(0, len(resposta)):
      if resposta[i] == '(':
          posicoesAberto.append(i)
      if resposta[i] == ')':
          ultimoRemovido = posicoesAberto.pop()
    return ultimoRemovido == 0 and resposta.endswith(')')

def ler_estados(arq):
    estados_string = arq.readline().strip()
    estados = estados_string.split(',')
    estados.append(ESTADO_INICIO)
    estados.append(ESTADO_FIM)
    return estados

def ler_simbolos(arq):
    simbolos_string = arq.readline().strip()
    simbolos = simbolos_string.split(',')
    return simbolos

def ler_estados_iniciais(arq):
    estados_iniciais_string = arq.readline().strip()
    estados_iniciais = estados_iniciais_string.split(',')
    return estados_iniciais

def ler_estados_finais(arq):
    estados_finais_string = arq.readline().strip()
    estados_finais = estados_finais_string.split(',')
    return estados_finais

def inicializa_grafo(estados, estados_iniciais, estados_finais):
    grafo = {}
    for estado1 in estados:
      grafo[estado1] = {}
      for estado2 in estados:
          grafo[estado1][estado2] = ''
    for estado in estados_iniciais:
      grafo[ESTADO_INICIO][estado] = LAMBDA

    for estado in estados_finais:
      grafo[estado][ESTADO_FIM] = LAMBDA
    return grafo

def construir_automato():
    arq = open(sys.argv[1])
    estados = ler_estados(arq)
    simbolos = ler_simbolos(arq)
    estados_iniciais = ler_estados_iniciais(arq)
    estados_finais = ler_estados_finais(arq)

    grafo = inicializa_grafo(estados, estados_iniciais, estados_finais)

    for linha in arq:
      lista = linha.strip().split(',')
      for el in lista[2:]:
          if grafo[lista[0]][el]:
            grafo[lista[0]][el]+=' + ' + lista[1]
          else: 
            grafo[lista[0]][el]=lista[1]
    
    arq.close()
    return (grafo, estados)

def estado_valido_saida(estado_saida, estado_removido, grafo, removidos):
    return grafo[estado_removido][estado_saida] and estado_removido != estado_saida and estado_saida not in removidos

def estado_valido_entrada(estado_entrada, estado_removido, grafo, removidos):
    return grafo[estado_entrada][estado_removido] and estado != estado_entrada and estado_entrada not in removidos

def obter_transicao_entrada(estado_entrada, estado_removido, grafo):
    if grafo[estado_entrada][estado_removido] != LAMBDA:
        if precisa_parenteses_para_concatenar(grafo[estado_entrada][estado_removido]):
            return '('+grafo[estado_entrada][estado_removido]+')'
        else:
            return grafo[estado_entrada][estado_removido]
    return ''

def obter_transicao_self_loop(self_loop, estado_removido, grafo):
    if self_loop:
        return '('+grafo[estado_removido][estado_removido]+')*'
    return ''

def obter_transicao_saida(estado_saida, estado_removido, grafo):
    if grafo[estado_removido][estado_saida]!= LAMBDA:
        if precisa_parenteses_para_concatenar(grafo[estado_removido][estado_saida]):
            return '('+grafo[estado_removido][estado_saida]+')'
        else:
            return grafo[estado_removido][estado_saida]
    return ''

def obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo):
    if grafo[estado_entrada][estado_saida]:
        return grafo[estado_entrada][estado_saida]+' + '+nova_aresta
    return nova_aresta

grafo, estados = construir_automato()

removidos = set()

# Remove os estados
for estado_removido in estados[:-2]:
    self_loop = False
    if grafo[estado_removido][estado_removido]:
      self_loop = True
    for estado_entrada in estados:
      if estado_valido_entrada(estado_entrada, estado_removido, grafo, removidos)
          for estado_saida in estados:
            if estado_valido_saida(estado_saida, estado_removido, grafo, removidos):
                nova_aresta = ''
                
                nova_aresta += obter_transicao_entrada(estado_entrada, estado_removido, grafo)
                nova_aresta += obter_transicao_self_loop(self_loop, estado_removido, grafo)
                nova_aresta += obter_transicao_saida(estado_saida, estado_removido, grafo)
                
                if nova_aresta == '':
                  nova_aresta = LAMBDA
                
                grafo[estado_entrada][estado_saida] = obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo)
                
    for estado in estados:
      grafo[estado][estado_removido] = ''
      grafo[estado_removido][estado] = ''
    removidos.add(estado)

resposta = grafo[ESTADO_INICIO][ESTADO_FIM]
while tem_parenteses_nas_pontas(resposta):
    resposta = resposta[1:-1]
print(resposta)

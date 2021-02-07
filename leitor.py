import sys

'''
Módulo responsável por ler o arquivo de entrada e construir a representação 
do AF como um diagrama ER representado por um grafo
'''

# Define constantes usadas no código
ESTADO_INICIO = 'estado_inicio_unico'
ESTADO_FIM = 'estado_fim_unico'
LAMBDA = 'λ'

# Le os estados do AF
def __ler_estados(arq):
    estados_string = arq.readline().strip()
    estados = estados_string.split(',')
    # Adiciona o estado inicial e final únicos criados para o algoritmo na lista de estados
    estados.append(ESTADO_INICIO)
    estados.append(ESTADO_FIM)
    return estados

# Le os símbolos do alfabeto
def __ler_simbolos(arq):
    simbolos_string = arq.readline().strip()
    simbolos = simbolos_string.split(',')
    return simbolos

# Le os estados iniciais do AF
def __ler_estados_iniciais(arq):
    estados_iniciais_string = arq.readline().strip()
    estados_iniciais = estados_iniciais_string.split(',')
    return estados_iniciais

# Le os estados finais do AF
def __ler_estados_finais(arq):
    estados_finais_string = arq.readline().strip()
    estados_finais = estados_finais_string.split(',')
    return estados_finais

# Inicializa o grafo usado para representar o diagrama ER
def inicializa_grafo(estados, estados_iniciais, estados_finais):
    grafo = {}
    # Inicializa o grafo como matriz de adjascência vazio
    for estado1 in estados:
        grafo[estado1] = {}
        for estado2 in estados:
            grafo[estado1][estado2] = ''
    # Define uma transição lambda entre o estado inicial único e os estados iniciais do AF
    for estado in estados_iniciais:
        grafo[ESTADO_INICIO][estado] = LAMBDA

    # Define uma transição lambda entre o estado final único e os estados finais do AF
    for estado in estados_finais:
        grafo[estado][ESTADO_FIM] = LAMBDA
    return grafo

def __constroi_grafo(arq, estados, estados_iniciais, estados_finais):
    grafo = inicializa_grafo(estados, estados_iniciais, estados_finais)

    # Le as transições do AF e adiciona cada transição como valor da aresta do grafo
    for linha in arq:
      lista = linha.strip().split(',')
      # Define que a transição com o símbolo vazio é uma transição lambda
      if lista[1] == '':
          lista[1] = LAMBDA
      for el in lista[2:]:
          if grafo[lista[0]][el]:
            # Caso mais de um símbolo faça a mesma transição, tranforma a transição  
            # na expressão regular composta pelos símbolos das transições separados por +
            grafo[lista[0]][el]+=' + ' + lista[1]
          else: 
            grafo[lista[0]][el]=lista[1]
    return grafo

def construir_automato():
    # Abre o arquivo recebido por argumento pelo programa
    arq = open(sys.argv[1])
    estados = __ler_estados(arq)
    simbolos = __ler_simbolos(arq)
    estados_iniciais = __ler_estados_iniciais(arq)
    estados_finais = __ler_estados_finais(arq)
    grafo = __constroi_grafo(arq, estados, estados_iniciais, estados_finais)
    # Fecha o arquivo após finalizar a leitura dos dados
    arq.close()
    return (grafo, estados)
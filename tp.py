#!/usr/bin/python3

import sys

# Define constantes usadas no código
ESTADO_INICIO = 'estado_inicio_unico'
ESTADO_FIM = 'estado_fim_unico'
LAMBDA = 'lambda'

# Le os estados do AF
def ler_estados(arq):
    estados_string = arq.readline().strip()
    estados = estados_string.split(',')
    # Adiciona o estado inicial e final únicos criados para o algoritmo na lista de estados
    estados.append(ESTADO_INICIO)
    estados.append(ESTADO_FIM)
    return estados

# Le os símbolos do alfabeto
def ler_simbolos(arq):
    simbolos_string = arq.readline().strip()
    simbolos = simbolos_string.split(',')
    return simbolos

# Le os estados iniciais do AF
def ler_estados_iniciais(arq):
    estados_iniciais_string = arq.readline().strip()
    estados_iniciais = estados_iniciais_string.split(',')
    return estados_iniciais

# Le os estados finais do AF
def ler_estados_finais(arq):
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

def constroi_grafo(arq, estados, estados_iniciais, estados_finais):
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
    estados = ler_estados(arq)
    simbolos = ler_simbolos(arq)
    estados_iniciais = ler_estados_iniciais(arq)
    estados_finais = ler_estados_finais(arq)
    grafo = constroi_grafo(arq, estados, estados_iniciais, estados_finais)
    # Fecha o arquivo após finalizar a leitura dos dados
    arq.close()
    return (grafo, estados)

def estado_valido_saida(estado_saida, estado_removido, grafo):
    # Determina se o estado pode ser considerado um estado de saída válido, 
    # ou seja, se existe a transição estado_removido -> estado_saida no diagrama ER atual
    return grafo[estado_removido][estado_saida] and estado_removido != estado_saida

def estado_valido_entrada(estado_entrada, estado_removido, grafo):
    # Determina se o estado pode ser considerado um estado de entrada válido, 
    # ou seja, se existe a transição estado_entrada -> estado_removido no diagrama ER atual
    return grafo[estado_entrada][estado_removido] and estado_removido != estado_entrada

# Verifica se a expressão regular enviada no paramêtro pode ser concatenada,
# sem alterar seu significado, com outra expressão sem utilizar parênteses
def precisa_parenteses_para_concatenar(atual):
    # Verifica se existe algum operador + fora de parênteses na ER atual
    # Caso exista, essa ER não pode ser concatenada sem os parênteses
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
    # Verifica se toda a ER está envolta por parentêses
    # Nesse caso esses parênteses podem ser removidos
    posicoesAberto = []
    ultimoRemovido = -1
    for i in range(0, len(resposta)):
      if resposta[i] == '(':
          posicoesAberto.append(i)
      if resposta[i] == ')':
          ultimoRemovido = posicoesAberto.pop()
    return ultimoRemovido == 0 and resposta.endswith(')')

# Processa o estado de entrada do diagrama ER para obter a ER de sua
# transição para o estado_removido
def obter_transicao_entrada(estado_entrada, estado_removido, grafo):
    # Caso a transição seja lambda, não adiciona nada na nova aresta
    if grafo[estado_entrada][estado_removido] != LAMBDA:
        # Caso a transição possa ser concatenado sem parênteses, concatena sem
        # os parênteses, caso contrário, coloca os parênteses
        if precisa_parenteses_para_concatenar(grafo[estado_entrada][estado_removido]):
            return '('+grafo[estado_entrada][estado_removido]+')'
        else:
            return grafo[estado_entrada][estado_removido]
    return ''

# Obtém a ER da transição do self loop do estado removido
def obter_transicao_self_loop(self_loop, estado_removido, grafo):
    # Se o estado tem um self loop
    if self_loop:
        return '('+grafo[estado_removido][estado_removido]+')*'
    return ''

# Processa o estado de saida do diagrama ER para obter a ER da
# transição do estado_removido
def obter_transicao_saida(estado_saida, estado_removido, grafo):
    # Caso a transição seja lambda, não adiciona nada na nova aresta
    if grafo[estado_removido][estado_saida]!= LAMBDA:
        # Caso a transição possa ser concatenado sem parênteses, concatena sem
        # os parênteses, caso contrário, coloca os parênteses
        if precisa_parenteses_para_concatenar(grafo[estado_removido][estado_saida]):
            return '('+grafo[estado_removido][estado_saida]+')'
        else:
            return grafo[estado_removido][estado_saida]
    return ''

# Processa o valor atual da transição entre estado_entrada e estado_saida
# para adicionar a nova ER obtida ao remover o estado_removido
def obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo):
    # Caso já exista uma transição entre estado_entrada e estado_saida
    # Adiciona a ER obtida com a ER já existente com o operador +
    if grafo[estado_entrada][estado_saida]:
        return grafo[estado_entrada][estado_saida]+' + '+nova_aresta
    return nova_aresta

# Calcula o valor #p(e) para todos os estados que podem ser removidos
# Esse valor é usado para remover os estados em ordem crescente de #p(e)
def calcularNumeroPares(grafo, estados):
    numero_pares = []
    for estado_removido in estados[:-2]:
        contador = 0
        for estado_entrada in estados:
            if estado_valido_entrada(estado_entrada, estado_removido, grafo):
                for estado_saida in estados:
                    if estado_valido_saida(estado_saida, estado_removido, grafo):
                        contador+=1
        # Adiciona o par (#p(e), e) na lista
        numero_pares.append((contador, estado_removido))
    # Ordena os pares, para os valores ficarem em ordem crescente de #p(e)
    numero_pares.sort()
    return numero_pares

# Executa o algoritmo para obter a ER a partir do diagrama ER
# construído a partir do AF
def remover_estados(grafo, estados):
    removidos = set()
    # Obtém os pares (#p(e), e) ordenados
    estados_pares = calcularNumeroPares(grafo, estados)
    # Remove todos os estados diferente do estado final e inicial único
    # Remove na ordem de menor #p(e), seguindo a eurística sugerida no livro
    # para obter ER menores
    for pares, estado_removido in estados_pares:
        # Determina se o estado sendo removido possui um self loop
        self_loop = False
        if grafo[estado_removido][estado_removido]:
            self_loop = True
        # Itera pelos possíveis estados de entrada e saída, tal que existe a transição:
        # estado_entrada  -> estado_removido -> estado_saida
        for estado_entrada in estados:
            if estado_valido_entrada(estado_entrada, estado_removido, grafo) and estado_entrada not in removidos:
                for estado_saida in estados:
                    if estado_valido_saida(estado_saida, estado_removido, grafo) and estado_saida not in removidos:
                        # Inicialmente a nova aresta não possui nenhuma ER
                        nova_aresta = ''
                        # Forma a ER da nova aresta
                        nova_aresta += obter_transicao_entrada(estado_entrada, estado_removido, grafo)
                        nova_aresta += obter_transicao_self_loop(self_loop, estado_removido, grafo)
                        nova_aresta += obter_transicao_saida(estado_saida, estado_removido, grafo)
                        # Caso a nova aresta não possua ER, ela é uma transição lambda
                        if nova_aresta == '':
                            nova_aresta = LAMBDA
                        # Insere a ER da nova aresta como transição entre estado_entrada e estado_saida
                        grafo[estado_entrada][estado_saida] = obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo)

        # Remove o estado_removido do diagrama ER   
        for estado in estados:
            grafo[estado][estado_removido] = ''
            grafo[estado_removido][estado] = ''
        removidos.add(estado_removido)
    return grafo

# Processa a ER obtida como resposta
def obter_resposta(grafo):
    resposta = grafo[ESTADO_INICIO][ESTADO_FIM]
    # Remove possíveis parênteses redundantes nas pontas da resposta
    while tem_parenteses_nas_pontas(resposta):
        resposta = resposta[1:-1]
    return resposta

# Programa principal
grafo, estados = construir_automato()
grafo = remover_estados(grafo, estados)
resposta = obter_resposta(grafo)
# Imprime a ER obtida
print(resposta)

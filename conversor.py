'''
Módulo responsável por converter o AF, representado como um diagrama ER, 
para uma expressão regular
'''

# Define constantes usadas no código
ESTADO_INICIO = 'estado_inicio_unico'
ESTADO_FIM = 'estado_fim_unico'
LAMBDA = 'λ'
VAZIO = '∅'

def __estado_valido_saida(estado_saida, estado_removido, grafo):
    # Determina se o estado pode ser considerado um estado de saída válido, 
    # ou seja, se existe a transição estado_removido -> estado_saida no diagrama ER atual
    return grafo[estado_removido][estado_saida] and estado_removido != estado_saida

def __estado_valido_entrada(estado_entrada, estado_removido, grafo):
    # Determina se o estado pode ser considerado um estado de entrada válido, 
    # ou seja, se existe a transição estado_entrada -> estado_removido no diagrama ER atual
    return grafo[estado_entrada][estado_removido] and estado_removido != estado_entrada

# Verifica se a expressão regular enviada no paramêtro pode ser concatenada com outra expressão
# sem utilizar parênteses e sem alterar seu significado
def __precisa_parenteses_para_concatenar(atual):
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

def __tem_parenteses_nas_pontas(resposta):
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
def __obter_transicao_entrada(estado_entrada, estado_removido, grafo):
    # Caso a transição seja lambda, não adiciona nada na nova aresta
    if grafo[estado_entrada][estado_removido] != LAMBDA:
        # Caso a transição possa ser concatenado sem parênteses, concatena sem
        # os parênteses, caso contrário, coloca os parênteses
        if __precisa_parenteses_para_concatenar(grafo[estado_entrada][estado_removido]):
            return '('+grafo[estado_entrada][estado_removido]+')'
        else:
            return grafo[estado_entrada][estado_removido]
    return ''

# Obtém a ER da transição do self loop do estado removido
def __obter_transicao_self_loop(self_loop, estado_removido, grafo):
    # Se o estado tem um self loop
    if self_loop:
        return '('+grafo[estado_removido][estado_removido]+')*'
    return ''

# Processa o estado de saida do diagrama ER para obter a ER da
# transição do estado_removido
def __obter_transicao_saida(estado_saida, estado_removido, grafo):
    # Caso a transição seja lambda, não adiciona nada na nova aresta
    if grafo[estado_removido][estado_saida]!= LAMBDA:
        # Caso a transição possa ser concatenado sem parênteses, concatena sem
        # os parênteses, caso contrário, coloca os parênteses
        if __precisa_parenteses_para_concatenar(grafo[estado_removido][estado_saida]):
            return '('+grafo[estado_removido][estado_saida]+')'
        else:
            return grafo[estado_removido][estado_saida]
    return ''

# Processa o valor atual da transição entre estado_entrada e estado_saida
# para adicionar a nova ER obtida ao remover o estado_removido
def __obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo):
    # Caso já exista uma transição entre estado_entrada e estado_saida
    # Adiciona a ER obtida com a ER já existente com o operador +
    if grafo[estado_entrada][estado_saida]:
        return grafo[estado_entrada][estado_saida]+' + '+nova_aresta
    return nova_aresta

# Calcula o valor #p(e) para todos os estados que podem ser removidos
# Esse valor é usado para remover os estados em ordem crescente de #p(e)
def __calcular_numero_pares(grafo, estados):
    numero_pares = []
    for estado_removido in estados[:-2]:
        contador = 0
        for estado_entrada in estados:
            if __estado_valido_entrada(estado_entrada, estado_removido, grafo):
                for estado_saida in estados:
                    if __estado_valido_saida(estado_saida, estado_removido, grafo):
                        contador+=1
        # Adiciona o par (#p(e), e) na lista
        numero_pares.append((contador, estado_removido))
    # Ordena os pares, para os valores ficarem em ordem crescente de #p(e)
    numero_pares.sort()
    return numero_pares

# Processa a ER obtida como resposta
def __obter_resposta(grafo):
    resposta = grafo[ESTADO_INICIO][ESTADO_FIM]
    # Remove possíveis parênteses redundantes nas pontas da resposta
    while __tem_parenteses_nas_pontas(resposta):
        resposta = resposta[1:-1]
    # Determina que caso a resposta seja a linguagem vazia, a saída deve ser o símbolo de vazio
    if resposta == '':
        resposta = VAZIO
    return resposta

# Executa o algoritmo para obter a ER a partir do diagrama ER
# construído a partir do AF
def converter_af_para_er(grafo, estados):
    # Obtém os pares (#p(e), e) ordenados
    estados_pares = __calcular_numero_pares(grafo, estados)
    # Remove todos os estados diferente do estado final e inicial único
    # Remove na ordem de menor #p(e), seguindo a heurística sugerida no livro
    # para obter ER menores
    for pares, estado_removido in estados_pares:
        # Determina se o estado sendo removido possui um self loop
        self_loop = False
        if grafo[estado_removido][estado_removido]:
            self_loop = True
        # Itera pelos possíveis estados de entrada e saída, tal que existe a transição:
        # estado_entrada  -> estado_removido -> estado_saida
        for estado_entrada in estados:
            if __estado_valido_entrada(estado_entrada, estado_removido, grafo):
                for estado_saida in estados:
                    if __estado_valido_saida(estado_saida, estado_removido, grafo):
                        # Inicialmente a nova aresta não possui nenhuma ER
                        nova_aresta = ''
                        # Forma a ER da nova aresta
                        nova_aresta += __obter_transicao_entrada(estado_entrada, estado_removido, grafo)
                        nova_aresta += __obter_transicao_self_loop(self_loop, estado_removido, grafo)
                        nova_aresta += __obter_transicao_saida(estado_saida, estado_removido, grafo)
                        # Caso a nova aresta não possua ER, ela é uma transição lambda
                        if nova_aresta == '':
                            nova_aresta = LAMBDA
                        # Insere a ER da nova aresta como transição entre estado_entrada e estado_saida
                        grafo[estado_entrada][estado_saida] = __obter_nova_aresta(estado_entrada, estado_saida, nova_aresta, grafo)

        # Remove o estado_removido do diagrama ER   
        for estado in estados:
            grafo[estado][estado_removido] = ''
            grafo[estado_removido][estado] = ''
    return __obter_resposta(grafo)

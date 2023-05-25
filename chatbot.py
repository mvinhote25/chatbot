# Construção do chatbot com Deep NLP

# Instalação das bibliotecas

import numpy as np
import tensorflow as tf
import re  # Para fazer o REGEX
import time

# ------------------------------------------------------------------------------
# -------------------- Parte 1: Pré-processamento dos dados --------------------
# ------------------------------------------------------------------------------


# Importamos as bases de dados

linhas = open('movie_lines.txt', encoding='utf-8', errors = 'ignore').read().split('\n')
conversas = open('movie_conversations.txt', encoding='utf-8', errors = 'ignore').read().split('\n')


# Criamos um dicionário para mapear cada linha com seu ID

id_para_linha = {}

for linha in linhas:
    _linha = linha.split(' +++$+++ ')
    if len(_linha) == 5:
        id_para_linha[_linha[0]] = _linha[4]


# for key, value in id_para_linha.items():
#    print(key,'----------',value)


# Criamos uma lista com todas as conversas

conversas_id = []

for conversa in conversas[:-1]:
    # print(conversa)
    _conversa = conversa.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    # print(_conversa)
    conversas_id.append(_conversa.split(","))



# Separação das perguntas e respostas
# 194 - 195 - 196 - 197

# 194 - 195
# 195 - 196
# 196 - 197


perguntas = []
respostas = []

for conversa in conversas_id:
    # print(conversa)
    # print('******')
    for i in range(len(conversa)-1):
        perguntas.append(id_para_linha[conversa[i]])
        respostas.append(id_para_linha[conversa[i+1]])



# ---------- Tratamento dos textos ----------


def limpa_texto(texto):
    texto = texto.lower()
    texto = texto.replace(r"i'm", "I am")
    texto = texto.replace(r"he's", "he is")
    texto = texto.replace(r"she's", "she is")
    texto = texto.replace(r"that's", "that is")
    texto = texto.replace(r"what's", "what is")
    texto = texto.replace(r"where's", "where is")
    texto = texto.replace(r"\'ll", " will")
    texto = texto.replace(r"\'ve", " have")
    texto = texto.replace(r"\'re", " are")
    texto = texto.replace(r"\'d", " would")
    texto = texto.replace(r"won't", "will not")
    texto = texto.replace(r"can't", "can not")
    texto = texto.replace(r"[-()#@;+={}~|]?", "")

    return texto


# Limpeza das perguntas

perguntas_limpas = []

for pergunta in perguntas:
    perguntas_limpas.append(limpa_texto(pergunta))
    
      
# for perg in perguntas_limpas:
#    print(perg)
    

    
# Limpeza das respostas

respostas_limpas = []

for resposta in respostas:
    respostas_limpas.append(limpa_texto(resposta))




# Criamos um dicionário que mapeia cada palavra e o número de ocorrência da mesma

palavras_contagem = {}

for pergunta in perguntas_limpas:
    for palavra in pergunta.split():
        if palavra not in palavras_contagem:
            palavras_contagem[palavra] = 1
        else:
            palavras_contagem[palavra] += 1
            
            
for resposta in respostas_limpas:
    for palavra in resposta.split():
        if palavra not in palavras_contagem:
            palavras_contagem[palavra] = 1
        else:
            palavras_contagem[palavra] += 1


# Removemos palavras que não são tão frequentes assim... 

limite = 20

perguntas_palavras_int = {}
numero_palavra = 0
for palavra, contagem in palavras_contagem.items():
    if contagem >= limite:
        perguntas_palavras_int[palavra] = numero_palavra
        numero_palavra += 1
        

respostas_palavras_int = {}
numero_palavra = 0
for palavra, contagem in palavras_contagem.items():
    if contagem >= limite:
        respostas_palavras_int[palavra] = numero_palavra
        numero_palavra += 1


# Adição de tokens nos dicionários

tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']

for token in tokens:
    perguntas_palavras_int[token] = len(perguntas_palavras_int) + 1
    respostas_palavras_int[token] = len(respostas_palavras_int) + 1


# Criação do dicionário inverso com o dicionário de respostas

respostas_int_palavras = {p_i: p for p, p_i in respostas_palavras_int.items()}


# Adição do token final de string <EOS> para o final de cada resposta

for i in range(len(respostas_limpas)):
    respostas_limpas[i] += ' <EOS>'
    

# Tradução de todas as perguntas e respostas para inteiros
# Substituição das palavras menos frequentes para <OUT>

perguntas_para_int = []
for pergunta in perguntas_limpas:
    ints = []
    for palavra in pergunta.split():
        if palavra not in perguntas_palavras_int:
            ints.append(perguntas_palavras_int['<OUT>'])
        else:
            ints.append(perguntas_palavras_int[palavra])
    perguntas_para_int.append(ints)


respostas_para_int = []
for resposta in respostas_limpas:
    ints = []
    for palavra in resposta.split():
        if palavra not in respostas_palavras_int:
            ints.append(respostas_palavras_int['<OUT>'])
        else:
            ints.append(respostas_palavras_int[palavra])
    respostas_para_int.append(ints)



# Ordenação das perguntas e respostas pelo tamanho das perguntas

perguntas_limpas_ordenadas = []
respostas_limpas_ordenadas = []
for tamanho in range(1,25+1):
    for i in enumerate(perguntas_para_int):
        if len(i[1]) == tamanho:
            perguntas_limpas_ordenadas.append(perguntas_para_int[i[0]])
            respostas_limpas_ordenadas.append(respostas_para_int[i[0]])
            
            


            
            
            
            
            






            
            













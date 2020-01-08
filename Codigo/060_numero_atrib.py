import pandas as pd
from Codigo import utils_og 

# lendo os dados
orgaos_atual = pd.read_csv('Amostra_Dados/Processados/df_atual.csv')
dic_atual = pd.read_csv('Amostra_Dados/Processados/dic_atual.csv')

orgaos_futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv')
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']

#Atual
       

p5_atual = utils_og.p5(dados = orgaos_atual, orgaos = n_orgao)
p5_atual.to_csv('Docs/Respostas/P5_atual.csv', encoding = 'ISO-8859-1')
#futuro

p5_futuro = utils_og.p5(dados = orgaos_futuro, orgaos = n_orgao)
p5_futuro.to_csv('Docs/Respostas/P5_futuro.csv', encoding = 'ISO-8859-1')
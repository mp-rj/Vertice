import pandas as pd
from Codigo import utils_og 

# lendo os dados
orgaos_atual = pd.read_csv('Amostra_Dados/Processados/df_atual.csv')
dic_atual = pd.read_csv('Amostra_Dados/Processados/dic_atual.csv')

orgaos_futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv')
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']

#Hoje
p2_atual = utils_og.f2(dados = orgaos_atual,dic = dic_atual, orgaos = n_orgao)

n_atrib_atual = orgaos_atual[orgaos_atual['Órgão'] != orgaos_atual['Quem faz']]\
    .groupby('Órgão')['Atribuição']\
    .nunique()\
    .reset_index()

p2_atual = p2_atual['quem_falou'].value_counts()\
     .reset_index()\
     .rename(columns = {'index':'Órgão'})      

p2_atual = p2_atual.merge(n_atrib_atual, on = 'Órgão', how='inner')\
    .assign(porcentagem = lambda x: round(x['quem_falou']/x['Atribuição'], 2)*100)    

p2_atual.to_csv('Docs/Respostas/P2_atual.csv', encoding = 'ISO-8859-1')

#Futuro
p2_futuro = utils_og.f2(dados = orgaos_futuro,dic = dic_futuro, orgaos = n_orgao)

n_atrib_futuro = orgaos_futuro[orgaos_futuro['Órgão'] != orgaos_futuro['Quem faz']]\
    .groupby('Órgão')['Atribuição']\
    .nunique()\
    .reset_index()

p2_futuro = p2_futuro['quem_falou'].value_counts()\
     .reset_index()\
     .rename(columns = {'index':'Órgão'})      

p2_futuro = p2_futuro.merge(n_atrib_futuro, on = 'Órgão', how='inner')\
    .assign(porcentagem = lambda x: round(x['quem_falou']/x['Atribuição'], 2)*100)    

p2_futuro.to_csv('Docs/Respostas/P2_futuro.csv', encoding = 'ISO-8859-1')
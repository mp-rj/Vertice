import pandas as pd
from Codigo import utils_og 

# lendo os dados
orgaos_atual = pd.read_csv('Amostra_Dados/Processados/df_atual.csv')
dic_atual = pd.read_csv('Amostra_Dados/Processados/dic_atual.csv')

orgaos_futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv')
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']


#Atual

p1_atual = utils_og.f1(dados = orgaos_atual,dic = dic_atual, orgaos = n_orgao)

n_atrib_atual = orgaos_atual[orgaos_atual['Órgão'] == orgaos_atual['Quem faz']]\
    .groupby('Órgão')['Atribuição']\
    .nunique()\
    .reset_index()

p1_atual = p1_atual['Quem_faz'].value_counts()\
     .reset_index()\
     .rename(columns = {'index':'Órgão'})
p1_atual['Órgão'] = [x[0] for x in p1_atual['Órgão']]       

p1_atual = p1_atual.merge(n_atrib_atual, on = 'Órgão', how='inner')\
    .assign(porcentagem = lambda x: round(x['Quem_faz']/x['Atribuição'], 2)*100)    

p1_atual.to_csv('Docs/Respostas/P1_atual.csv', encoding = 'ISO-8859-1')

#futuro
p1_futuro =  utils_og.f1(dados = orgaos_futuro,dic = dic_futuro, orgaos = n_orgao)

n_atrib_futuro = orgaos_futuro[orgaos_futuro['Órgão'] == orgaos_futuro['Quem faz']]\
    .groupby('Órgão')['Atribuição']\
    .nunique()\
    .reset_index()

p1_futuro = p1_futuro['Quem_faz'].value_counts()\
     .reset_index()\
     .rename(columns = {'index':'Órgão'})
p1_futuro['Órgão'] = [x[0] for x in p1_futuro['Órgão']]       

p1_futuro = p1_futuro.merge(n_atrib_futuro, on = 'Órgão', how='inner')\
    .assign(porcentagem = lambda x: round(x['Quem_faz']/x['Atribuição'], 2)*100) 

p1_futuro.to_csv('Docs/Respostas/P1_futuro.csv', encoding = 'ISO-8859-1')
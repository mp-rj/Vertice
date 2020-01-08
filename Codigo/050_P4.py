import pandas as pd
from Codigo import utils_og 

# lendo os dados
orgaos_atual = pd.read_csv('Amostra_Dados/Processados/df_atual.csv')
dic_atual = pd.read_csv('Amostra_Dados/Processados/dic_atual.csv')

orgaos_futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv')
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']

#Atual

p4_atual_final = pd.DataFrame()

for orgao in n_orgao:

    p2_atual = utils_og.f2(dados = orgaos_atual,dic = dic_atual, orgaos = n_orgao)
    p2_atual['Quem_faz'] = [x[0] for x in p2_atual['Quem_faz']]
    p2_atual = p2_atual[p2_atual['Quem_faz'] == orgao].drop_duplicates(['Id_atrib'])

    p4_atual = orgaos_atual[(orgaos_atual['Órgão'] == orgao) & (orgaos_atual['Quem faz'] == orgao)].drop_duplicates(['Atribuição'])\
        .merge(p2_atual, on = 'Atribuição', how = 'inner')\
        .drop(['Grupo', 'Quem faz'], axis = 1)

    total_atrib_n_consolid_atual = orgaos_atual[(orgaos_atual['Órgão'] == orgao) & (orgaos_atual['Quem faz'] == orgao)]\
        .drop_duplicates(['Atribuição'])['Órgão']\
        .value_counts()\
        .reset_index()\
        .rename(columns = {'Órgão':'total_N_consolidado'})           


    p4_atual = (p4_atual['Quem_faz']
        .value_counts()
        .reset_index()
        .rename(columns = {'Quem_faz':'N_consolidado'})    
        .merge(total_atrib_n_consolid_atual, on = 'index', how = 'inner')
        .assign(Porcentagem = lambda x: round(x['N_consolidado']/x['total_N_consolidado'], 2)*100))

    p4_atual_final = p4_atual_final.append(p4_atual)            

p4_atual_final.to_csv('Docs/Respostas/P4_atual.csv', encoding = 'ISO-8859-1')

#futuro

p4_futuro_final = pd.DataFrame()

for orgao in n_orgao:

    p2_futuro = utils_og.f2(dados = orgaos_futuro,dic = dic_futuro, orgaos = n_orgao)
    p2_futuro['Quem_faz'] = [x[0] for x in p2_futuro['Quem_faz']]
    p2_futuro = p2_futuro[p2_futuro['Quem_faz'] == orgao].drop_duplicates(['Id_atrib'])

    p4_futuro = orgaos_futuro[(orgaos_futuro['Órgão'] == orgao) & (orgaos_futuro['Quem faz'] == orgao)].drop_duplicates(['Atribuição'])\
        .merge(p2_futuro, on = 'Atribuição', how = 'inner')\
        .drop(['Grupo', 'Quem faz'], axis = 1)

    total_atrib_n_consolid_futuro = orgaos_futuro[(orgaos_futuro['Órgão'] == orgao) & (orgaos_futuro['Quem faz'] == orgao)]\
        .drop_duplicates(['Atribuição'])['Órgão']\
        .value_counts()\
        .reset_index()\
        .rename(columns = {'Órgão':'total_N_consolidado'})           


    p4_futuro = (p4_futuro['Quem_faz']
        .value_counts()
        .reset_index()
        .rename(columns = {'Quem_faz':'N_consolidado'})    
        .merge(total_atrib_n_consolid_futuro, on = 'index', how = 'inner')
        .assign(Porcentagem = lambda x: round(x['N_consolidado']/x['total_N_consolidado'], 2)*100))

    p4_futuro_final = p4_futuro_final.append(p4_futuro)    

p4_futuro_final.to_csv('Docs/Respostas/P4_futuro.csv', encoding = 'ISO-8859-1')    
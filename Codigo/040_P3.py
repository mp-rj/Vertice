import pandas as pd
from Codigo import utils_og 

# lendo os dados
orgaos_atual = pd.read_csv('Amostra_Dados/Processados/df_atual.csv')
dic_atual = pd.read_csv('Amostra_Dados/Processados/dic_atual.csv')

orgaos_futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv')
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']

#Atual
p3_atual_final = pd.DataFrame()
for orgao in n_orgao:
    p1_atual = utils_og.f1(dados = orgaos_atual,dic = dic_atual, orgaos = n_orgao)
    p2_atual = utils_og.f2(dados = orgaos_atual,dic = dic_atual, orgaos = n_orgao)

    p1_atual['Quem_faz'] = [x[0] for x in p1_atual['Quem_faz']]
    p2_atual['Quem_faz'] = [x[0] for x in p2_atual['Quem_faz']]
 
    p2_atual = p2_atual[p2_atual['Quem_faz'] == orgao].drop_duplicates(['Id_atrib'])

    p3_atual = p1_atual[p1_atual['Quem_faz'] == orgao]['Id_atrib']\
                .reset_index()\
                .merge(p2_atual, on = 'Id_atrib', how = 'inner')   

    p3_atual = p3_atual['Quem_faz'].value_counts()\
                .reset_index()\
                .merge(p1_atual[p1_atual['Quem_faz'] == orgao]['Quem_faz'].value_counts().reset_index(), on = 'index', how = 'inner')\
                .assign(Porcentagem = lambda x: round(x['Quem_faz_x']/x['Quem_faz_y'], 2)*100)      

    p3_atual_final = p3_atual_final.append(p3_atual)

p3_atual_final.to_csv('Docs/Respostas/P3_atual.csv', encoding = 'ISO-8859-1')

#futuro
p3_futuro_final = pd.DataFrame()  
for orgao in  n_orgao:                 
    p1_futuro = utils_og.f1(dados = orgaos_futuro,dic = dic_futuro, orgaos = n_orgao)
    p2_futuro = utils_og.f2(dados = orgaos_futuro,dic = dic_futuro, orgaos = n_orgao)

    p1_futuro['Quem_faz'] = [x[0] for x in p1_futuro['Quem_faz']]
    p2_futuro['Quem_faz'] = [x[0] for x in p2_futuro['Quem_faz']]

    p2_futuro = p2_futuro[p2_futuro['Quem_faz'] == orgao].drop_duplicates(['Id_atrib'])

    p3_futuro = p1_futuro[p1_futuro['Quem_faz'] == orgao]['Id_atrib']\
                .reset_index()\
                .merge(p2_futuro, on = 'Id_atrib', how = 'inner')   

    p3_futuro = p3_futuro['Quem_faz'].value_counts()\
                .reset_index()\
                .merge(p1_futuro[p1_futuro['Quem_faz'] == orgao]['Quem_faz'].value_counts().reset_index(), on = 'index', how = 'inner')\
                .assign(Porcentagem = lambda x: round(x['Quem_faz_x']/x['Quem_faz_y'], 2)*100)      

    p3_futuro_final = p3_futuro_final.append(p3_futuro)

p3_futuro_final.to_csv('Docs/Respostas/P3_futuro.csv', encoding = 'ISO-8859-1')    
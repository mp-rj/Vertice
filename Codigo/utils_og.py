import pandas as pd 
import numpy as np

def coesao_orgao(dados, orgao, interno=True):
    if interno:
        dados = dados[dados['Quem faz'] == orgao]
    else:
        dados = dados[dados['Quem faz'] != orgao]

    dados_trat = (dados
        .groupby(['Grupo', 'Atribuição'])
        .agg(quem = ('Quem faz',list))
        .pivot_table(index='Atribuição', columns='Grupo', values='quem', aggfunc=lambda x: list(x[0]))
        .reset_index()
        .rename(columns={1: 'Grupo_1', 2: 'Grupo_2'}))
    dados_trat['Grupo_1_s'] = dados_trat['Grupo_1'].apply(lambda x: np.sort(x, axis = None))    
                
    dados_trat['Visao'] = [np.array_equal(x,y) for x,y in zip(dados_trat['Grupo_1_s'],dados_trat['Grupo_2'])]       
   
    return dados_trat    

def f1(dados, dic, orgaos):
    import pandas as pd
    df = pd.DataFrame()
    for orgao in orgaos:
        df_1 = dados[dados['Órgão'] == orgao]
        df_1 = coesao_orgao(dados=df_1, orgao=orgao)\
        .query('Visao == True')\
        .merge(dic, on='Atribuição', how='left')\
        .rename(columns={'Grupo_1': 'Quem_faz'})[['Quem_faz', 'Id_atrib', 'Atribuição']]

        df = df.append(df_1)
    return df 

def f2(dados, dic, orgaos):

    df = pd.DataFrame()
    for orgao in orgaos:
        df_1 = dados[dados['Órgão'] == orgao]
        df_1 = (coesao_orgao(dados=df_1, orgao=orgao, interno = False)
            .query('Visao == True') 
            .merge(dic, on='Atribuição', how='left')
            .assign(quem_falou = orgao) 
            .rename(columns={'Grupo_1': 'Quem_faz'})[['quem_falou', 'Quem_faz', 'Id_atrib', 'Atribuição']])
        df = df.append(df_1)    
    return df 

def p5(dados, orgaos):

    df = pd.DataFrame()
    for orgao in orgaos:
         df_aux = (dados[dados['Quem faz'] == orgao]
                   .groupby('Atribuição')
                   .agg(Quem_falou = ('Órgão',list),
                        Quem_faz = ('Quem faz',list))
                   .reset_index() 
                   .assign(Quantidade_qf = lambda x: x['Quem_falou'].apply(lambda x: len(x)),
                        Quem_faz = lambda x: x['Quem_faz'].apply(lambda x: np.unique(x)[0]))
                   )
         df = df.append(df_aux)  
    return df    

#função de decisão para quebras naturais. Como é necessário ter ao menos 3 elementos, quando isso acontece retornamos o máximo entre os 3 elementos. 
#quando não acontece, utilizamos o algoritmo de quebras naturais
def decision(lista):
    import jenkspy as jk

    lista_sem_na = lista[~np.isnan(lista)]    
    if len(lista_sem_na) < 4:
        quebra = max(lista_sem_na)
    else:
        quebra = jk.jenks_breaks(lista_sem_na, nb_class = 3)[-2]
    return quebra       
import pandas as pd
from Codigo import utils_og, decision 
import numpy as np

futuro = pd.read_csv('Amostra_Dados/Processados/df_futuro.csv').drop_duplicates()
dic_futuro = pd.read_csv('Amostra_Dados/Processados/dic_futuro.csv')[['Atribuição', 'Id_atrib']]

n_orgao = ['GATE', 'CENPE', 'CADG', 'STIC', 'CSI', 'IEP', 'INOVA']

#P1: Para cada orgão, ver atribuições convergentes
#P2: Agrupar, por atribuição, os orgãos que irão faze-las (segundo eles mesmos)
#P3: Fazer a contagem de quantos grupos acham que a atribuição é papel de cada orgão que a tomou para si. Excluindo o orgão que falou
#P4: São selecionados os orgãos que receberam o número de votos acima do terceiro quartil 


#----------#
#Para cada orgão, aplicar a função coesao que retorna a variável dummy Visão para opninões iguais entre grupos do mesmo orgão
passo_1 = pd.DataFrame()
for orgao in n_orgao:
    df = utils_og.coesao_orgao(dados = futuro[futuro['Órgão'] == orgao], orgao = orgao).query('Visao == True')
    passo_1 = passo_1.append(df)

#----------#
#Com apenas as atribuições convergentes nos orgãos, agrupamos por atribuição os orgão que disseram ter essa atribuição
passo_2 = (passo_1.assign(og = lambda x: x['Grupo_2'].apply(lambda x: x[0])).drop(['Grupo_1', 'Grupo_2', 'Visao'], axis = 1)
    .groupby('Atribuição')
    .agg(og_tot = ('og', list))
    .reset_index())
#----------#
   

#Após fazermos uma cópia dos dados agrupados por atribuição, geramos a contagem dos grupos, para cada atribuição, dos orgaos que eles disseram que tem a atribuição

passo_3_1 = passo_2.copy().reset_index()
passo_3_2 = (passo_2['Atribuição']
        .apply(lambda x: futuro[futuro['Atribuição'] == x]['Quem faz'].value_counts())
        .assign(percent = lambda x: x.apply(lambda x: decision(x),axis = 1)))

#Utilizando a quebra natural, listamos os orgaos que segundos a opniao de todos tem a atribuição

og_list = pd.DataFrame(columns= ['Orgaos'])
for row in range(1,len(passo_3_1)+1):

    percent_orgao = passo_3_2['percent'][row-1]
    lista_orgaos = passo_3_1['og_tot'][row-1]
    lista_percent_orgaos = (passo_3_2[row-1:row].drop('percent', axis = 1)
                            .apply(lambda row: (row >= percent_orgao), axis = 1))
                           
    lista_percent_orgaos = (passo_3_2[row-1:row].drop('percent', axis = 1)
                            .columns[lista_percent_orgaos.apply(lambda x: x == True).values[0]].values.tolist())

    og_list = og_list.append({'Orgaos': lista_percent_orgaos}, ignore_index = True)

#----------#
#Neste último passo fazemos a interseção entre os orgãos que se auto atribuiram algo com a opnião de todos os grupos sobre quem deve ter tal atribuição

passo_4 = (passo_3_1.merge(og_list.reset_index(), on = 'index', how = 'left')
            .drop('index', axis = 1)
            .assign(Resultado = lambda x: x[['og_tot', 'Orgaos']].apply(lambda row: np.intersect1d(row['og_tot'], row['Orgaos']), axis = 1))
            .drop(['og_tot', 'Orgaos'], axis = 1)) 

passo_4.to_csv('Docs/Respostas/algo.csv', encoding = 'ISO-8859-1')













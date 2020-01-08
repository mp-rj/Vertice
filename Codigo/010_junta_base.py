import numpy as np
import pandas as pd

#definindo dir das bases
cadg = 'Amostra_Dados/Crus/Dataset_CADG.xlsx'
cenpe = 'Amostra_Dados/Crus/Dataset_CENPE.xlsx'
gate = 'Amostra_Dados/Crus/Dataset_GATE.xlsx'
stic = 'Amostra_Dados/Crus/Dataset_STIC.xlsx'
csi =  'Amostra_Dados/Crus/Dataset_CSI.xlsx'
iep =  'Amostra_Dados/Crus/Dataset_IEP.xlsx'
inova = 'Amostra_Dados/Crus/Dataset_INOVA.xlsx'
orgaos = [cadg, cenpe, gate, stic, csi, iep, inova]
 
def ler_bases(path, tempo):
    data = pd.read_excel(path, tempo, skiprows = 1)
    return data

#Lendo arquivos
df_atual = pd.DataFrame()
df_futuro = pd.DataFrame()
for og in orgaos:
    df_a = ler_bases(path = og, tempo = 'Atual')
    df_f = ler_bases(path = og, tempo = 'Futuro')
    df_futuro = df_futuro.append(df_f)
    df_atual = df_atual.append(df_a)
   

#criando dicionários 
dic_atual = df_atual.drop_duplicates('Atribuição')
dic_atual['Id_atrib'] = np.arange(1,dic_atual.shape[0] +1)

dic_futuro = df_futuro.drop_duplicates('Atribuição')
dic_futuro['Id_atrib'] = np.arange(1,dic_futuro.shape[0] +1)

#escrevendo os dados
df_atual.to_csv('Amostra_Dados/Processados/df_atual.csv', index = False)
df_futuro.to_csv('Amostra_Dados/Processados/df_futuro.csv', index = False)

dic_atual.to_csv('Amostra_Dados/Processados/dic_atual.csv', index = False)
dic_futuro.to_csv('Amostra_Dados/Processados/dic_futuro.csv', index = False)
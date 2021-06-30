#-*- coding: utf-8 -*-
"""
Created on Wed Mar 10 09:07:31 2021

@author: FMDias
"""

import pandas as pd
import numpy as np
import os

#https://concla.ibge.gov.br/classificacoes/correspondencias/produtos.html

#importando arquivo xlsx
Prod_2006x2005 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2006 X PRODLIST-Ind 2005.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2006,2005,'Atualização'])


Prod_2007x2006 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2007 X PRODLIST-Ind 2006.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2007,2006,'Atualização'])


Prod_2010x2007 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2010 X PRODLIST-Ind 2007.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2010,2007,'Atualização'])


Prod_2013x2010 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2013 X PRODLIST-Ind 2010.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2013,2010,'Atualização'])


Prod_2016x2013 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2016 X PRODLIST-Ind 2013.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2016,2013,'Atualização'])

Prod_2019x2016 = pd.read_excel(
    os.path.join(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\Prodlists', 'PRODLIST-Ind 2019 X PRODLIST-Ind 2016.xlsx'),
     engine='openpyxl', sheet_name = 0, header = 0, dtype=str, usecols=[1,3,4], names = [2019,2016,'Atualização'])



''' Criando Função para cruzar bases ProdList'''

def ano_base_2010(tabela_base, ano_atual, ano_novo, ProdList_anos):
    """ anos precisam ser seguidos, por exemplo: 2010, 2007; 2010,2013; 2005,2006"""
   
    #Tomando 2010 como base e agregando os outros anos
    Base_2010 = tabela_base
   
    #Adicionando coluna de Atualização para base nova
    Base_2010 = Base_2010.merge(ProdList_anos[[ano_atual, "Atualização"]], how = 'left', on = ano_atual)
   
    #Códigos para alteração ou não de prodlist
    alterou = ['DG','AG / AA','AG','AG ','AC/AN','AC / AN / AM','AC','AC / AM',
               'AC / AM / AN','AC / AN', 'AA','AA / AC','AA / AC / AN','AA / AD',
               'AA / AD / AM','AA / AD / AN','AA / AD / AN / AM','AA / AM','AA / AN',
               'AA / AN / AM','AA/AC/AN','AA/AD','AA/AD/AN','AA/AD/AN/AM','AA/AN']
   
    nao_alterou = [' ','  ','AN/AM','AN / AM','AM','AM / AN','AN', 'AD',
                   'AD / AM','AD / AM / AN','AD / AN','AD / AN / AM','AD/AN',
                   'AD/AN/AM','E','I',np.nan]
   
   
    #MARCANDO SE ALTEROU OU NÃO
    Base_2010["Mudou?"] = ["sim" if Base_2010['Atualização'][i] in alterou else "não" for i in range(len(Base_2010))]
    Base_2010["AG/DG?"] = ["sim" if Base_2010['Atualização'][i] in ['DG','AG / AA','AG','AG '] else "não" for i in range(len(Base_2010))]
    Base_2010["E/I?"] = ["sim" if Base_2010['Atualização'][i] in ['E','I'] else "não" for i in range(len(Base_2010))]
       
       
    #Adicionando ano novo
    lista_ano_novo = []
    for i in range(len(Base_2010)):
        if Base_2010["Mudou?"][i] == "sim" and Base_2010["AG/DG?"][i] == "não":
            ano = ProdList_anos[ProdList_anos[ano_atual] == Base_2010[ano_atual][i]].reset_index(drop = True)[ano_novo][0]
            lista_ano_novo.append(ano)
           
        elif Base_2010["Mudou?"][i] == "sim" and Base_2010["AG/DG?"][i] == "sim":
            lista_ano_novo.append("AG/DG")
           
        elif Base_2010["Mudou?"][i] == "não" and Base_2010["E/I?"][i] == 'não':
            lista_ano_novo.append(Base_2010[ano_atual][i])
           
        elif Base_2010["Mudou?"][i] == "não" and Base_2010["E/I?"][i] == 'sim':
            lista_ano_novo.append("E/I")
   
    Base_2010[ano_novo] = lista_ano_novo
   
   
   
    '''Organizando códigos Agregados ou Desagregados'''
   
    #HÁ DIFERENÇAS SE O ANO ATUAL ESTÁ ATRÁS OU NA FRENTE DO ANO NOVO
    if ano_atual > ano_novo : #buscando anos anteriores ao ano base
       
        #Separando códigos com agregação ou desagregação
        Agregados = Base_2010[Base_2010[ano_novo] == "AG/DG"].copy()
       
        #Removendo colunas de AG e DG do Base_2010
        Base_2010 = Base_2010.drop(index = Agregados.index)
       
       
        #Criando um DataFrame para os códigos agregados e desagregados
        lista_ano_novo_agdg = pd.DataFrame(columns = [ano_atual, 'Atualização', 'Mudou?', 'AG/DG?', "E/I?", ano_novo])
       
        for i in Agregados.index:
            if Agregados["Atualização"][i] in ['AG / AA','AG','AG ']:
                count = len(ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]])
                for j in range(count):
                    lista_ano_novo_agdg = lista_ano_novo_agdg.append({ano_atual: Agregados[ano_atual][i],
                            'Atualização': Agregados['Atualização'][i],
                            'Mudou?': Agregados['Mudou?'][i],
                            'AG/DG?': Agregados['AG/DG?'][i],
                            'E/I?': Agregados['E/I?'][i],
                            ano_novo: ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]].reset_index(drop = True)[ano_novo][j]}, ignore_index=True)            
                   
            elif Agregados["Atualização"][i] == "DG":
               
                codigo = ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]].reset_index(drop = True)[ano_novo][0]
                count = len(ProdList_anos[ProdList_anos[ano_novo] == codigo])
               
                for j in range(count):
                    lista_ano_novo_agdg = lista_ano_novo_agdg.append({ano_atual: ProdList_anos[ProdList_anos[ano_novo] == codigo].reset_index(drop = True)[ano_atual][j],
                            'Atualização': Agregados['Atualização'][i],
                            'Mudou?': Agregados['Mudou?'][i],
                            'AG/DG?': Agregados['AG/DG?'][i],
                            'E/I?': Agregados['E/I?'][i],
                            ano_novo: ProdList_anos[ProdList_anos[ano_novo] == codigo].reset_index(drop = True)[ano_novo][j]}, ignore_index=True)            
       
       
    elif  ano_novo > ano_atual:   #buscando anos após o ano base
        #Separando códigos com agregação ou desagregação
        Agregados = Base_2010[Base_2010[ano_novo] == "AG/DG"].copy()
       
        #Removendo colunas de AG e DG do Base_2010
        Base_2010 = Base_2010.drop(index = Agregados.index)
       
       
        #Criando um DataFrame para os códigos agregados e desagregados
        lista_ano_novo_agdg = pd.DataFrame(columns = [ano_atual, 'Atualização', 'Mudou?', 'AG/DG?', "E/I?", ano_novo])
       
        for i in Agregados.index:
            if Agregados["Atualização"][i] == "DG":
                count = len(ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]])
                for j in range(count):
                    lista_ano_novo_agdg = lista_ano_novo_agdg.append({ano_atual: Agregados[ano_atual][i],
                            'Atualização': Agregados['Atualização'][i],
                            'Mudou?': Agregados['Mudou?'][i],
                            'AG/DG?': Agregados['AG/DG?'][i],
                            'E/I?': Agregados['E/I?'][i],
                            ano_novo: ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]].reset_index(drop = True)[ano_novo][j]}, ignore_index=True)            
                 
                   
            if Agregados["Atualização"][i] in ['AG / AA','AG','AG ']:
               
                codigo = ProdList_anos[ProdList_anos[ano_atual] == Agregados[ano_atual][i]].reset_index(drop = True)[ano_novo][0]
                count = len(ProdList_anos[ProdList_anos[ano_novo] == codigo])
               
                for j in range(count):
                    lista_ano_novo_agdg = lista_ano_novo_agdg.append({ano_atual: ProdList_anos[ProdList_anos[ano_novo] == codigo].reset_index(drop = True)[ano_atual][j],
                            'Atualização': Agregados['Atualização'][i],
                            'Mudou?': Agregados['Mudou?'][i],
                            'AG/DG?': Agregados['AG/DG?'][i],
                            'E/I?': Agregados['E/I?'][i],
                            ano_novo: ProdList_anos[ProdList_anos[ano_novo] == codigo].reset_index(drop = True)[ano_novo][j]}, ignore_index=True)            


    #Adicionando colunas dos outros anos a base 'lista_ano_novo_agdg'
    outros_anos = Agregados.drop(columns = {'Atualização','Mudou?','AG/DG?','E/I?',ano_novo})
    lista_ano_novo_agdg = lista_ano_novo_agdg.merge(outros_anos, how = 'left', on = ano_atual) #vai duplicar, mas não tem problema pois iremos remover os duplicados no final

   
    '''Organizando códigos Excluídos ou Incluídos'''
   
    #HÁ DIFERENÇAS SE O ANO ATUAL ESTÁ ATRÁS OU NA FRENTE DO ANO NOVO
    if ano_atual > ano_novo : #buscando anos anteriores ao ano base
       
        #Separando códigos  excluidos ou incluidos
        In_Excluidos = Base_2010[Base_2010[ano_novo] == "E/I"].copy()
       
       
        #Removendo colunas de AG e DG do Base_2010
        Base_2010 = Base_2010.drop(index = In_Excluidos.index)
       
        #Cuidando dos códigos excluidos de um ano para outro
        #len(ProdList_anos[ProdList_anos['Atualização'] == 'I'])
       
        #Criando um DataFrame para os códigos excluido e incluidos
        lista_ano_novo_i = pd.DataFrame(columns = [ano_atual, 'Atualização', 'Mudou?', 'AG/DG?', ano_novo])
       
       
        for i in In_Excluidos.index:
            if In_Excluidos["Atualização"][i] == 'I':
                lista_ano_novo_i = lista_ano_novo_i.append({ano_atual: In_Excluidos[ano_atual][i],
                        'Atualização': In_Excluidos['Atualização'][i],
                        'Mudou?': In_Excluidos['Mudou?'][i],
                        'AG/DG?': In_Excluidos['AG/DG?'][i],
                        'E/I?': In_Excluidos['E/I?'][i],
                        ano_novo: '----'}, ignore_index=True)            
               
               
        Excluidos = ProdList_anos[ProdList_anos["Atualização"] == "E"][[ano_novo, 'Atualização']]  
        Excluidos['Mudou?'] = ['não']*len(Excluidos)
        Excluidos['AG/DG?'] = ['não']*len(Excluidos)
        Excluidos['E/I?'] = ['sim']*len(Excluidos)
        Excluidos[ano_atual] = ['----']*len(Excluidos)
               
        lista_ano_novo_i = pd.concat([lista_ano_novo_i, Excluidos])
       
       
    elif  ano_novo > ano_atual:   #buscando anos após o ano base
        #Separando códigos  excluidos ou incluidos
        In_Excluidos = Base_2010[Base_2010[ano_novo] == "E/I"].copy()
       
       
        #Removendo colunas de AG e DG do Base_2010
        Base_2010 = Base_2010.drop(index = In_Excluidos.index)
       
        #Cuidando dos códigos excluidos de um ano para outro
        #len(ProdList_anos[ProdList_anos['Atualização'] == 'I'])
       
        #Criando um DataFrame para os códigos excluido e incluidos
        lista_ano_novo_i = pd.DataFrame(columns = [ano_atual, 'Atualização', 'Mudou?', 'AG/DG?', ano_novo])
       
       
        for i in In_Excluidos.index:
            if In_Excluidos["Atualização"][i] == 'E':
                lista_ano_novo_i = lista_ano_novo_i.append({ano_atual: In_Excluidos[ano_atual][i],
                        'Atualização': In_Excluidos['Atualização'][i],
                        'Mudou?': In_Excluidos['Mudou?'][i],
                        'AG/DG?': In_Excluidos['AG/DG?'][i],
                        'E/I?': In_Excluidos['E/I?'][i],
                        ano_novo: '----'}, ignore_index=True)            
               
               
        Incluidos = ProdList_anos[ProdList_anos["Atualização"] == "I"][[ano_novo, 'Atualização']]  
        Incluidos['Mudou?'] = ['não']*len(Incluidos)
        Incluidos['AG/DG?'] = ['não']*len(Incluidos)
        Incluidos['E/I?'] = ['sim']*len(Incluidos)
        Incluidos[ano_atual] = ['----']*len(Incluidos)
               
        lista_ano_novo_i = pd.concat([lista_ano_novo_i, Incluidos])

   
   
    #Adicionando colunas dos outros anos a base 'lista_ano_novo_i'
    outros_anos = In_Excluidos.drop(columns = {'Atualização','Mudou?','AG/DG?','E/I?',ano_novo})
    lista_ano_novo_i = lista_ano_novo_i.merge(outros_anos, how = 'left', on = ano_atual) #vai duplicar, mas não tem problema pois iremos remover os duplicados no final
    #Para os anos sem correspondência nos outros anos, adicionar '----'
    lista_ano_novo_i = lista_ano_novo_i.fillna('----')
       
    # Juntando as duas bases
    Base_2010 = pd.concat([Base_2010, lista_ano_novo_agdg, lista_ano_novo_i])
   
    #Selecionando apenas colunas com os anos
    Base_2010 = Base_2010.drop(columns = ['Atualização','Mudou?','AG/DG?','E/I?'])
   
    #Removendo duplicatas
    Base_2010 = Base_2010.drop_duplicates().reset_index(drop = True)
   
   
    return Base_2010
   
 

'''           UTILIZAÇÃO DA FUNÇÃO             '''


tabela_base = Prod_2010x2007[[2010]]
ano_novo = 2007
ano_atual = 2010
ProdList_anos = Prod_2010x2007

tabela_base1 = ano_base_2010(tabela_base, ano_atual, ano_novo, ProdList_anos) #3600


ano_novo = 2006
ano_atual = 2007
ProdList_anos = Prod_2007x2006

tabela_base2 = ano_base_2010(tabela_base1, ano_atual, ano_novo, ProdList_anos) #3947

ano_novo = 2005
ano_atual = 2006
ProdList_anos = Prod_2006x2005

tabela_base3 = ano_base_2010(tabela_base2, ano_atual, ano_novo, ProdList_anos) #4130


ano_novo = 2013
ano_atual = 2010
ProdList_anos = Prod_2013x2010

tabela_base4 = ano_base_2010(tabela_base3, ano_atual, ano_novo, ProdList_anos) #4140


ano_novo = 2016
ano_atual = 2013
ProdList_anos = Prod_2016x2013

tabela_base5 = ano_base_2010(tabela_base4, ano_atual, ano_novo, ProdList_anos) #4167



ano_novo = 2019
ano_atual = 2016
ProdList_anos = Prod_2019x2016

tabela_base6 = ano_base_2010(tabela_base5, ano_atual, ano_novo, ProdList_anos) #4197




## EXPORTANDO BASE FINAL COM DADOS ENTRE 2005 e 2019 PARA EXCEL
tabela_base6.to_excel(r'C:\Users\femdi\OneDrive\Documentos\Python\Codigos\ProdList\ProdLists Relação entre anos 2005 a 2019.xlsx')



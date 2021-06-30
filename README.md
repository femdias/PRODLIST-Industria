# PRODLIST-Industria

Uma função para relacionar as classificações PRODLIST-Industria do IBGE de um ano para outro.


A PRODLIST-Industria "é uma lista detalhada de bens e serviços industriais investigados pela Pesquisa Industrial Anual - Produto, PIA-Produto do IBGE" com códigos de oito dígitos no formato xxxx.xxxx. A grande dificuldade desse sistema é que de um ano para outro (de divulgação da PIA) esses códigos mudam, o que dificulta muito relacionar uma sequência grande de anos.

Essa função recebe uma tabela base (uma tabela com uma coluna de códigos PRODLIST de algum ano), o ano atual (ano da tabela base), o ano novo (ano cujas prodlists você queira adicionar) e a tabela de relação dos PRODLISTs do ano atual com o ano novo. Essas tabelas de relação podem ser achadas em https://concla.ibge.gov.br/classificacoes/correspondencias/produtos.html . Ela retorna a tabela base acrescida dos códigos PRODLIST do ano novo. Cada linha dessa tabela sempre será única.  



### English

A function to relate all IBGE's PRODLIST-Industria classification from one year to another.


PRODLIST-Industria "is a detailed list of industrial goods and services used in IBGE's Annual Industrial Survey - Product, PIA-Product" with eight-digit codes in the format xxxx.xxxx. The greatest difficulty with this system is that from one year to another (of PIAs) these codes change, which makes it very difficult to relate a long sequence of years.

This function receives a base table (a table with a column of PRODLIST codes from some year), the current year (year of the base table), the new year (year whose prodlists you want to add) and the PRODLISTs relation table of the year current with the new year. These relation tables can be found at https://concla.ibge.gov.br/classificacoes/correspondencias/produtos.html . It returns the base table plus the new year's PRODLIST codes. Each row in this table will always be unique.






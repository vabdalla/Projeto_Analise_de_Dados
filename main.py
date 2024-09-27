#   Projeto Analise de Dados empresa de prestação de Serviços
#   1 - Valor total da folha salarial -> Qual foi o gasto total com salários de funcionários pela empresa?
#   2 - Qual foi o faturamento da empresa?
#   3 - Qual a % de funcionários que ja fechou algum contrato?
#   4 - Calcule o total de contratos que cada área da empresa já fechou
#   5 - Calcule o total de funcionários por área
#   6 - Qual o ticket médio mensal (faturamento médio mensal) dos contratos?

from itertools import groupby
import pandas as pd

#LER PLANILHAS E ARMAZENAR EM VARIAVEIS
servicos_prestados_df = pd.read_excel('BaseServiçosPrestados.xlsx')
cadastro_clientes_df = pd.read_csv("CadastroClientes.csv", sep = ';', decimal = ',')
cadastro_funcionarios_df = pd.read_csv("CadastroFuncionarios.csv", sep = ';', decimal = ',')


#   1 - Valor total da folha salarial -> Qual foi o gasto total com salários de funcionários pela empresa?

#adicionar coluna Salario Total com a soma de Salario,Impostos e Beneficios
cadastro_funcionarios_df['Salario Total'] = cadastro_funcionarios_df[['Salario Base', 'Impostos',
                                                                             'Beneficios']].sum(axis=1)
folha_salarial_total = sum(cadastro_funcionarios_df['Salario Total'])
print(f'    1 - GASTO TOTAL = R${folha_salarial_total}')

#   2 - Qual foi o faturamento da empresa?

#Utilizando o pd.merge() para linkar as 2 planilhas serviços_prestados e cadastro_clientes pela coluna em comum
#ID Cliente
nova_planilha = pd.merge(servicos_prestados_df, cadastro_clientes_df
[['ID Cliente', 'Valor Contrato Mensal']], on = 'ID Cliente', how = 'left')

#Cria nova coluna TOTAL VALOR CONTRATO multiplicando o valor de contrato mensal pelo tempo total de contrato
nova_planilha['TOTAL VALOR CONTRATO'] = nova_planilha['Tempo Total de Contrato (Meses)'] * nova_planilha['Valor Contrato Mensal']

#Soma da coluna TOTAL VALOR CONTRATO
faturamento_total = sum(nova_planilha['TOTAL VALOR CONTRATO'])
print(f'    2 - FATURAMENTO TOTAL: R${faturamento_total}')


#   3 - Qual a % de funcionários que ja fechou algum contrato?
funcionarios_que_fecharam = nova_planilha['ID Funcionário'].unique().tolist()
todos_os_funcionarios = cadastro_funcionarios_df['ID Funcionário'].unique().tolist()
nao_fecharam = set(todos_os_funcionarios) - set(funcionarios_que_fecharam)
percentual_que_nao_fechou = (len(funcionarios_que_fecharam)*100) / len(todos_os_funcionarios)
print(f'    3 - {percentual_que_nao_fechou:.2f}% dos funcionários já fecharam algum contrato')


#   4 - Calcule o total de contratos que cada área da empresa já fechou
nova_planilha = pd.merge(nova_planilha, cadastro_funcionarios_df[['ID Funcionário','Area']], on='ID Funcionário', how='left')
total_de_contratos_area = nova_planilha['Area'].value_counts()
print()
print('     4 - TOTAL DE CONTRATOS QUE CADA AREA FECHOU ')
print(total_de_contratos_area)

#   5 - Calcule o total de funcionários por área
total_de_funcionarios_area = cadastro_funcionarios_df['Area'].value_counts()
print()
print('     5 - TOTAL DE FUNCIONÁRIOS POR ÁREA')
print(total_de_funcionarios_area)

#   6 - Qual o ticket médio mensal (faturamento médio mensal) dos contratos?
ticket_medio_mensal = cadastro_clientes_df['Valor Contrato Mensal'].mean()
print()
print(f'    6 - TICKET MEDIO MENSAL: R${ticket_medio_mensal:.2f}')
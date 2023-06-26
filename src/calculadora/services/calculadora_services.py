from telnetlib import STATUS
from flask import jsonify
from sqlalchemy import create_engine, true
from sqlalchemy.orm import sessionmaker
# from src.models.db_clientes import Clientes
# from src.models.db_formasPagamento import FormasPagamentos
# from src.models.db_enterprisesCodes import EnterprisesCodes
# from main import db
import datetime as dt
import os
# from dotenv import load_dotenv, find_dotenv
import asyncio
import ast
import pandas as pd
from dateutil.relativedelta import *
import math
import ast
import math
import numpy
from sqlalchemy import desc, true, asc

class prep_dados():

    def primeiro_dia_do_proximo_mes(self,primeiro_dia_do_mes_que_vem):
        primeiro_dia_do_mes_que_vem = primeiro_dia_do_mes_que_vem+relativedelta(months=+1)
        primeiro_dia_do_mes_que_vem = dt.date(primeiro_dia_do_mes_que_vem.year,primeiro_dia_do_mes_que_vem.month,1)
        return primeiro_dia_do_mes_que_vem

    def valida_datas(self,data_inicio_entrada,qtd_entradas,data_inicio_parciais,data_inicio_parcelas):
        hoje = dt.date.today()
        # primeiro_dia_do_mes_que_vem = dt.date(hoje.year, hoje.month+1, 1)
        primeiro_dia_do_mes_que_vem = self.primeiro_dia_do_proximo_mes(hoje)

        # - Data sinal tem que ser no mes do lançamento (se for a Ultima semana do mes pode ser no mes seguintes)
        if (hoje - primeiro_dia_do_mes_que_vem).days <= 7:
            if hoje.month != data_inicio_entrada.month and primeiro_dia_do_mes_que_vem.month != data_inicio_entrada.month:
                return False, 'Data de inicio de entrada não pode ser dois meses no futuro'
        else:
            if hoje.month != data_inicio_entrada.month:
                return False, 'Data de inicio de entrada não pode ser no mes seguinte'

        # - Data parcela/reduzidas tem que ser logo apos ao ultimo pagamento do sinal
        if str(data_inicio_parciais) != '0':
            
            data_depois_da_entrada = data_inicio_entrada + relativedelta(months=qtd_entradas)
            if data_inicio_parciais.month != data_depois_da_entrada.month or data_inicio_parciais.year != data_depois_da_entrada.year:
                return False, 'Data de inicio de reduzidas não pode ser no mes seguinte'
            
            data_depois_das_reduzidas = data_inicio_parciais + relativedelta(months=12)
            if data_inicio_parcelas.month != data_depois_das_reduzidas.month or data_inicio_parcelas.year != data_depois_das_reduzidas.year:
                return False, 'Data de inicio de parcelas não pode ser no mes seguinte'

            if data_inicio_parciais.day > 25:
                return False, 'Data de vencimento das reduzidas não pode ser após o dia 25'

        else:
            data_depois_da_entrada = data_inicio_entrada + relativedelta(months=qtd_entradas)
            if data_inicio_parcelas.month != data_depois_da_entrada.month or data_inicio_parcelas.year != data_depois_da_entrada.year:
                return False, 'Data de inicio de parcelas não pode ser no mes seguinte'

            if data_inicio_parcelas.day > 25:
                return False, 'Data de vencimento das parciais não pode ser após o dia 25'
        

        return True, 'Datas validadas com sucesso'

    def trata_retorno(self,valor_parcela,valor_reduzida,entrada_minima,valor_entrada,tem_parciais,tem_balao,valor_reduzida_sem_juros,qtd_balao,valor_balao_sem_juros):
        print('trata retorno')
        print(valor_parcela,valor_reduzida,entrada_minima,valor_entrada,tem_parciais,tem_balao,valor_reduzida_sem_juros,qtd_balao,valor_balao_sem_juros)
        # if valor_entrada < entrada_minima:
        #     treated_data = {
        #             'status':404,
        #             'message':'Entrada menor que o valor da entrada mínima! Escolha um valor maior ou igual a %s'%(entrada_minima), 
        #             'valor_entrada_proposto' : valor_entrada,
        #             'entrada_minima' : entrada_minima,
        #         }
        # else:
        valor_parcela = round(valor_parcela,2)
        if valor_parcela==valor_reduzida==entrada_minima==valor_entrada==tem_parciais==tem_balao==valor_reduzida_sem_juros==qtd_balao==valor_balao_sem_juros==0:
            treated_data = {
                        'status':404,
                        'message':'Estamos sofrendo instabilidades na comunicação com o Vimob. Pedimos sua paciência até que a situação se estabilize. Estamos trabalhando diretamente com a equipe do Vimob para lhe atender o quanto antes!'
                    }

        elif tem_parciais:
            treated_data = {
                        'status':200,
                        'message':'Calculo feito com sucesso!', 
                        'valor_parcela' : valor_parcela,
                        'valor_reduzidas' : valor_reduzida,
                        'entrada_minima' : entrada_minima,
                        'valor_reduzida_sem_juros':valor_reduzida_sem_juros
                    }
        elif tem_balao:
            treated_data = {
                        'status':200,
                        'message':'Calculo feito com sucesso!', 
                        'valor_parcela' : valor_parcela,
                        'valor_presente_balao' : valor_balao_sem_juros,
                        'entrada_minima' : entrada_minima,
                        'valor_reduzida_sem_juros':0,
                        'qtd_balao':qtd_balao
                    }
        else:
            treated_data = {
                        'status':200,
                        'message':'Calculo feito com sucesso!', 
                        'valor_parcela' : valor_parcela,
                        'valor_reduzidas' : valor_reduzida,
                        'entrada_minima' : entrada_minima,
                        'valor_reduzida_sem_juros':0
                        }

        treated_data_json = jsonify(treated_data)
        return treated_data,treated_data_json
    
    def str_to_date(self,data):
        # 2023-06-26
        print(data,data[4])
        if data[4]=='-':
            dia = str(data)[8:]
            mes = str(data)[5:7]
            ano = str(data)[:4]

        #06-26-2023
        else:
            dia = str(data)[:2]
            mes = str(data)[3:5]
            ano = str(data)[6:10]

        date =  dt.datetime(int(ano),int(mes),int(dia))
        return date

#================================DEPRECADO
    def entrada_minima_old(entrada,id_emp,valor_lote):
        if (id_emp == '1641'):
            entradaMinima = valor_lote * 0.0556
        elif (id_emp == '1523' or id_emp == '1548'):
            entradaMinima = valor_lote * 0.1
        elif (id_emp == '6416' or id_emp == '5406' or id_emp == '3412'):
            entradaMinima = valor_lote * 0.05
        elif (id_emp == '5435'):
            entradaMinima = valor_lote * 0.045
        else:
            entradaMinima = 0


        return entradaMinima
    
    def entrada_minima(self,id_emp,valor_lote,percent_entrada):
        print(id_emp,valor_lote,percent_entrada)
        if id_emp in ['2172','2193','2404']:
            if valor_lote<= 79900:entradaMinima = 3600
            elif valor_lote<= 99900:entradaMinima = 4800
            elif valor_lote<= 119900:entradaMinima = 6000
            elif valor_lote<= 199900:entradaMinima = 9000
            elif valor_lote<= 259900:entradaMinima = 12000
            else:entradaMinima = 15000
            
            return entradaMinima
        else:return valor_lote * percent_entrada

#================================DEPRECADO
class fluxo():
    def __init__(self):
        colunas = ['BOP','juros','saldoParcial','amortizacao','entrada','reduzida','parcela','EOP']
        self.df = pd.DataFrame(columns=colunas)

class main():
    def __init__(self):
        self.FLUXO = fluxo().df
        self.juros_amortizacao = ((1.12)**(1/12))-1
        # self.juros_amortizacao = 0.009489
        self.pd = prep_dados()
        # self.FormasDePagamento = FormasPagamentos()
        # self.codigosEmpreendimentos = EnterprisesCodes()
        self.hoje = dt.datetime.now()
        self.parcelasMinimasComBalao = {
            '5329':527,
            '937':527,
            '2032':527,
            '1':527
        }
    
    def npv(juros_amortizacao,listFluxo):
        sum_pv = 0  # <-- variable used to sum result

        for i, pmt in enumerate(listFluxo, start=1):  # <-- use of enumerate allows you to do away with the counter variables.
            sum_pv += pmt / ((1 + juros_amortizacao) ** i)  # <-- add pv of one of the cash flows to the sum variable

        return sum_pv  # <-- only return the sum after your loop has completed.

    def pgto(self,pv,i,n):
        pmt = (pv * i) / (1 - (1 + i) ** -n)
        return pmt

    def capta_dados_pagamento(self,id_emp):
        
        if int(id_emp) != 6416 : hashEmpreendimento = str(self.codigosEmpreendimentos.query.filter_by(enterprise_code=str(id_emp)).one()).replace('{','').replace('}','').replace("'enterprise_id': UUID",'').replace('(','').replace(')','').replace("'",'').split(',')[0]
        else: hashEmpreendimento = 'ed2f1cc2-047b-45c7-a831-9519bff5df41'
        CondicaoPagamentoEmpreendimento = trata_dict(self.FormasDePagamento.query.filter_by(id_empreendimento=str(hashEmpreendimento)).all())
        
        self.entradaMinima = float(CondicaoPagamentoEmpreendimento['entrada_minima'])
        self.quantidadeMaxParcelasEntrada = int(CondicaoPagamentoEmpreendimento['quantidade_max_parcelas_entrada'])
        self.quantidadeMaxParcelasMensal = int(CondicaoPagamentoEmpreendimento['quantidade_max_parcelas_mensal'])
        self.Reduzidas = bool(CondicaoPagamentoEmpreendimento['reduzidas'])
        self.CurtoSemJuros = bool(CondicaoPagamentoEmpreendimento['curto_sem_juros'])
        # self.balao = bool(CondicaoPagamentoEmpreendimento['balao'])
        self.balao = False
        # self.valorMaximoBalao = bool(CondicaoPagamentoEmpreendimento['valorMaximoBalao'])
        self.valorMaximoBalao = False

        # print(self.entradaMinima,self.quantidadeMaxParcelasEntrada,self.quantidadeMaxParcelasMensal,self.Reduzidas,self.CurtoSemJuros)

    def calcula_valor_reduzida_sem_juros(self,valor_reduzida,qtd_entrada):
        if qtd_entrada == 1: listFluxo = [0,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida]
        elif qtd_entrada == 2: listFluxo = [0,0,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida]
        elif qtd_entrada == 3: listFluxo = [0,0,0,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida,valor_reduzida]
        # print('REDUZIDA--------------->',valor_reduzida)
        # vpl = numpy.npv(self.juros_amortizacao,listFluxo)
        vpl = self.npv(self.juros_amortizacao,listFluxo)
        # print('VPL--------------->',vpl)

        return vpl/12
    
    def calcula_valor_balao_sem_juros(self,Fluxo_balao,qtd_baloes):
        # vpl = numpy.npv(self.juros_amortizacao,Fluxo_balao['balao'].values)
        vpl = self.npv(self.juros_amortizacao,Fluxo_balao['balao'].values)
        return (vpl/qtd_baloes)


    def corrige_valor_reduzida_com_juros(self,valor_reduzida,qtd_entrada,meses_juros):
        saldo_reduzidas = valor_reduzida*12
        saldo_reduzidas_corrigida = saldo_reduzidas*(1+self.juros_amortizacao)**((meses_juros))
        return saldo_reduzidas_corrigida/12


    def valida_dados_pagamento(self,percent_valor_entrada,tem_parciais,qtd_entradas,qtd_parcelas,tem_balao,valor_Balao,id_emp,valorLote):
        def casoCerejeiras(percente_valor_entrada,valor_lote):
            valorEntrada = percent_valor_entrada*valor_lote
            if valor_lote<= 79900:entradaMinima = 3600
            elif valor_lote<= 99900:entradaMinima = 4800
            elif valor_lote<= 119900:entradaMinima = 6000
            elif valor_lote<= 199900:entradaMinima = 9000
            elif valor_lote<= 259900:entradaMinima = 12000
            else:entradaMinima = 15000
            
            # print('CASO DO CEREJEIRAS',entradaMinima,valorEntrada,valorEntrada>=entradaMinima)
            return valorEntrada>=entradaMinima

        
        def trata_dict(dict):
            finalDict = {}
            dict = str(dict).replace('{','').replace('}','').split(',')
            
            for item in dict:
                item = item.split(':')
                key = item[0].replace("'",'').replace(' ','').replace('[','').replace(']','')
                value = item [1].replace("'",'').replace(' ','').replace('[','').replace(']','')

                if key == 'id' : 
                    id = value
                    finalDict[id] = {}
                else: finalDict[id][key] = value
            return finalDict

        def ordena_dict_pagamento(dict):
            list_vezes = []
            for idParcelamento in dict:
                formaPagamento = dict[idParcelamento]
                list_vezes.append(int(formaPagamento['quantidade_max_parcelas_mensal']))
            
            dict_final = {}
            menor_financiamento = min(list_vezes)
            
            for idParcelamento in dict:
                formaPagamento = dict[idParcelamento]
                if formaPagamento['quantidade_max_parcelas_mensal'] == menor_financiamento: dict_final[idParcelamento] = dict[idParcelamento]
            
            for idParcelamento in dict:
                formaPagamento = dict[idParcelamento]
                if formaPagamento['quantidade_max_parcelas_mensal'] != menor_financiamento: dict_final[idParcelamento] = dict[idParcelamento]
            return dict_final

        print(percent_valor_entrada)
        percent_valor_entrada = round(percent_valor_entrada,3)

        if int(id_emp) != 6416 : hashEmpreendimento = str(self.codigosEmpreendimentos.query.filter_by(enterprise_code=str(id_emp)).one()).replace('{','').replace('}','').replace("'enterprise_id': UUID",'').replace('(','').replace(')','').replace("'",'').split(',')[0]
        # query_token = str(Token.query.order_by(desc(Token.data_geracao)).first())
        
        else: hashEmpreendimento = 'ed2f1cc2-047b-45c7-a831-9519bff5df41'
        CondicaoPagamentoEmpreendimento = trata_dict(self.FormasDePagamento.query.filter_by(id_empreendimento=str(hashEmpreendimento)).order_by(asc(FormasPagamentos.quantidade_max_parcelas_mensal)).all())
        CondicaoPagamentoEmpreendimento = ordena_dict_pagamento(CondicaoPagamentoEmpreendimento)
        # retorno = [True,'Tudo ok','']
        problemaComEntrada = False
        print(CondicaoPagamentoEmpreendimento)
                
        for idParcelamento in CondicaoPagamentoEmpreendimento:
            formaPagamento = CondicaoPagamentoEmpreendimento[idParcelamento]        
            formaPagamento['entrada_minima'] = round(float(formaPagamento['entrada_minima']),2)
            #financiamento curto
            # if qtd_parcelas <= 24 and qtd_entradas == 1 and percent_valor_entrada>=0.1 and str(formaPagamento['curto_sem_juros']) == 'True':
            print(str(formaPagamento['curto_sem_juros']) , qtd_parcelas , int(formaPagamento['quantidade_max_parcelas_mensal']))

            if str(formaPagamento['curto_sem_juros']) == 'True' and (qtd_parcelas <= int(formaPagamento['quantidade_max_parcelas_mensal'])):
                retorno = [True,'Tudo ok','','','']
                print('=====================================financiamento_curto')
                # print(int(formaPagamento['quantidade_max_parcelas_mensal']))
                # print(formaPagamento)
                if str(formaPagamento['curto_sem_juros']) == 'False': self.CurtoSemJuros = False
                else: self.CurtoSemJuros = True
                # print(percent_valor_entrada,float(formaPagamento['entrada_minima']),percent_valor_entrada < float(formaPagamento['entrada_minima']),float(formaPagamento['entrada_minima']) != 0.0)
                if float(formaPagamento['entrada_minima']) != 0.0 and percent_valor_entrada < float(formaPagamento['entrada_minima']): retorno = [False,'Entrada mais baixa que o mínimo.','']
                elif tem_parciais == True and str(formaPagamento['reduzidas']) == 'False': retorno = [False, 'Este empreendimento nao permite reduzidas.','']
                elif qtd_entradas > int(formaPagamento['quantidade_max_parcelas_entrada']): retorno = [False, 'Mais parcelas de entrada do que o permitido para este empreendimento.','']
                elif qtd_parcelas > int(formaPagamento['quantidade_max_parcelas_mensal']): retorno = [False,  'Mais parcelas mensais do que o permitido para este empreendimento.','']

                elif self.CurtoSemJuros: 
                    return retorno
            
            #financiamento longo
            elif str(formaPagamento['curto_sem_juros']) != 'True':
                print('-------------------------------------------------------------------------------------------')
                print(int(formaPagamento['quantidade_max_parcelas_mensal']),int(formaPagamento['quantidade_max_parcelas_mensal'])>1,(tem_balao == False and str(formaPagamento['baloes']) == 'False'),(tem_parciais == False and str(formaPagamento['reduzidas']) == 'False'),tem_parciais == False , str(formaPagamento['reduzidas']) == 'False')


                if problemaComEntrada == False: retorno = [True,'Tudo ok','','',float(formaPagamento['entrada_minima'])]

                if id_emp in ['2172','2193','2404']:
                    formaPagamento['entrada_minima'] = self.pd.entrada_minima(id_emp,valorLote,float(formaPagamento['entrada_minima']))/valorLote

                #parciais
                if tem_parciais and str(formaPagamento['reduzidas']) != 'False':
                    print('=====================================financiamento_longo')
                    print('=========Reduzidas')
                    print(formaPagamento)
                    if percent_valor_entrada < float(formaPagamento['entrada_minima']): 
                        print('Entrada zuada')
                        problemaComEntrada = True
                        entrada_minima_do_caso = self.pd.entrada_minima(id_emp,valorLote,float(formaPagamento['entrada_minima']))
                        retorno = [False,'Entrada mais baixa que o mínimo: R$'+str(entrada_minima_do_caso),'','',float(formaPagamento['entrada_minima'])  ]
                    elif tem_parciais == True and str(formaPagamento['reduzidas']) == 'False' and percent_valor_entrada not in [0.05,0.08,0.1,0.15]: 
                        print('Parciais zuada')
                        retorno = [False, 'Este empreendimento nao permite reduzidas ou a entrada não esta de acordo.','','',float(formaPagamento['entrada_minima'])  ]
                    elif qtd_entradas > int(formaPagamento['quantidade_max_parcelas_entrada']): 
                        print('Qtd Entrada zuada')
                        retorno = [False, 'Mais parcelas de entrada do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])  ]
                    elif qtd_parcelas > int(formaPagamento['quantidade_max_parcelas_mensal']): 
                        print('Qtd de parcelas zuada. Possui',qtd_parcelas,'pode possuir',int(formaPagamento['quantidade_max_parcelas_mensal']))
                        if problemaComEntrada == False: retorno = [False,  'Mais parcelas mensais do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])  ]
                    else: 
                        print('else')
                        retorno = [True,'Tudo ok','','',float(formaPagamento['entrada_minima'])]
                        if str(formaPagamento['curto_sem_juros']) == 'False': self.CurtoSemJuros = False
                        else: self.CurtoSemJuros = True
                        return retorno 

                #balao
                elif tem_balao and str(formaPagamento['baloes']) != 'False':
                    print('=====================================financiamento_longo')
                    print('=========Balao')
                    print(formaPagamento)
                    if percent_valor_entrada < float(formaPagamento['entrada_minima']): 
                        print('Entrada zuada')
                        problemaComEntrada = True
                        entrada_minima_do_caso = self.pd.entrada_minima(id_emp,valorLote,float(formaPagamento['entrada_minima']))
                        retorno = [False,'Entrada mais baixa que o mínimo: R$'+str(entrada_minima_do_caso),'','',float(formaPagamento['entrada_minima'])  ]
                    elif qtd_entradas > int(formaPagamento['quantidade_max_parcelas_entrada']): 
                        print('Qtd Entrada zuada')
                        retorno = [False, 'Mais parcelas de entrada do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])  ]
                    elif qtd_parcelas > int(formaPagamento['quantidade_max_parcelas_mensal']): 
                        print('Qtd de parcelas zuada. Possui',qtd_parcelas,'pode possuir',int(formaPagamento['quantidade_max_parcelas_mensal']))
                        if problemaComEntrada == False: retorno = [False,  'Mais parcelas mensais do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])  ]
                    elif tem_balao == True and str(formaPagamento['baloes']) == 'False':
                        print('Balao zuado')
                        retorno = [False, 'Este empreendimento nao permite balões.','','',float(formaPagamento['entrada_minima'])  ]
                    else: 
                        print('else')
                        retorno = [True,'Tudo ok','','',float(formaPagamento['entrada_minima'])]
                        if str(formaPagamento['curto_sem_juros']) == 'False': self.CurtoSemJuros = False
                        else: self.CurtoSemJuros = True
                        return retorno 
                
    
                #convencional
                elif (tem_balao == False and str(formaPagamento['baloes']) == 'False') and (tem_parciais == False and str(formaPagamento['reduzidas']) == 'False') and int(formaPagamento['quantidade_max_parcelas_mensal'])>1:
                    print('=====================================financiamento_longo')
                    print('=========regular')
                    print(formaPagamento)
                    print(percent_valor_entrada , float(formaPagamento['entrada_minima']),formaPagamento['quantidade_max_parcelas_mensal'])
                    if percent_valor_entrada < float(formaPagamento['entrada_minima']): 
                        print('Entrada zuada')
                        problemaComEntrada = True
                        entrada_minima_do_caso = self.pd.entrada_minima(id_emp,valorLote,float(formaPagamento['entrada_minima']))
                        retorno = [False,'Entrada mais baixa que o mínimo: R$'+str(entrada_minima_do_caso),'','',float(formaPagamento['entrada_minima'])  ]
                    elif qtd_entradas > int(formaPagamento['quantidade_max_parcelas_entrada']): 
                        print('Qtd Entrada zuada')
                        retorno = [False, 'Mais parcelas de entrada do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])]
                    elif qtd_parcelas > int(formaPagamento['quantidade_max_parcelas_mensal']): 
                        print('Qtd de parcelas zuada. Possui',qtd_parcelas,'pode possuir',int(formaPagamento['quantidade_max_parcelas_mensal']))
                        if problemaComEntrada == False: retorno = [False,  'Mais parcelas mensais do que o permitido para este empreendimento.','','',float(formaPagamento['entrada_minima'])  ]
                    else: 
                        print('else')
                        retorno = [True,'Tudo ok','','',float(formaPagamento['entrada_minima'])]
                        if str(formaPagamento['curto_sem_juros']) == 'False': self.CurtoSemJuros = False
                        else: self.CurtoSemJuros = True
                        return retorno 


                # if tem_balao == True and formaPagamento['balao'] == False: retorno =[False, 'Este empreendimento nao permite baloes.','']
                # if valor_Balao > formaPagamento['valorBalao']: retorno =[False,'Balão mais alto que o máximo.','']
                
        print('==========================BOA')
        print(retorno)
        return retorno     

    def run_all(self,valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela,data_inicio_parciais,tem_balao,valor_balao,data_inicio_balao):
        # print('EMPREENDIMENTO',id_emp)
        
        # validacao = self.valida_dados_pagamento(percent_valor_entrada,tem_parciais,qtd_entradas,qtd_parcelas,tem_balao,valor_balao,id_emp,valor_lote)
        # print('validacao dos valores de pagamento',validacao,len(validacao))
        # entradaMinima = validacao[4]
        entradaMinima = 0.1
        # print(entradaMinima,validacao[0])
        validacao = [True]
        self.CurtoSemJuros = True

        if validacao[0]:
            print(qtd_parcelas <= 24 , qtd_entradas == 1 , percent_valor_entrada>=0.1 , self.CurtoSemJuros)
            if qtd_parcelas <= 24 and ((qtd_entradas == 1 and percent_valor_entrada>=0.1) or (qtd_entradas==0)) and self.CurtoSemJuros:
                print('prazo curto')
                valor_parcela,valor_reduzida,valores_totais = self.run_24x_sem_juros(valor_lote,percent_valor_entrada,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                return valor_parcela,valor_reduzida,valores_totais,0,0,0,0
            elif tem_parciais:
                print('reduzidas')
                # valor_parcela,valor_reduzida,valores_totais = self.run_v1(valor_lote,percent_valor_entrada,tem_parciais,tem_balao,valor_balao,data_inicio_entrada,data_inicio_balao,data_referencia_juros,qtd_entradas,qtd_parcelas,data_parcela)
                # valor_parcela,valor_reduzida,valores_totais = self.run_v2(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros = self.run_v3(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                return valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros,entradaMinima,0,0
            elif tem_balao:
                print('balao')
                # valor_parcela,vp_balao,valores_totais = self.run_v1(valor_lote,percent_valor_entrada,tem_parciais,tem_balao,valor_balao,data_inicio_entrada,data_inicio_balao,data_referencia_juros,qtd_entradas,qtd_parcelas,data_parcela)
                # return valor_parcela,vp_balao,valores_totais,0
                valor_parcela,valor_balao,valores_totais,qtd_balao,valor_balao_sem_juros = self.run_balao(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela,valor_balao,data_inicio_balao)
                return valor_parcela,valor_balao,valores_totais,0,entradaMinima,qtd_balao,valor_balao_sem_juros
            else:
                print('normal')
                # valor_parcela,valor_reduzida,valores_totais = self.run_v1(valor_lote,percent_valor_entrada,tem_parciais,tem_balao,valor_balao,data_inicio_entrada,data_inicio_balao,data_referencia_juros,qtd_entradas,qtd_parcelas,data_parcela)
                # valor_parcela,valor_reduzida,valores_totais = self.run_v2(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                # valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros = self.run_v3(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                # return valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros

                valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros = self.run_v3(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela)
                return valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros,entradaMinima,0,0
        else:
            validacao.append('')
            validacao.append('')
            return validacao
    #================================DEPRECADO
    def run(self,valor_lote,data_referencia_uros,qtd_entradas,percent_valor_entrada,data_inicio_entrada,tem_parciais,data_inicio_parciais,qtd_parcelas,data_inicio_parcelas,id_emp,data_parcela):
        self.FLUXO_fake = self.FLUXO.copy()

        qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = int(round((data_inicio_entrada - data_referencia_juros).days/30,0))
        if tem_parciais: 
            qtd_parcelas = qtd_parcelas - 12
            qtd_total_de_elementos = qtd_entradas + qtd_parcelas + qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + 12
        else:
            qtd_total_de_elementos = qtd_entradas + qtd_parcelas + qtd_meses_de_diferenca_entre_valor_referencia_e_entrada

        self.FLUXO.at[0,'BOP'] = valor_lote

        for elemento in range(0,qtd_total_de_elementos+1):
            if elemento < qtd_meses_de_diferenca_entre_valor_referencia_e_entrada:
                print('periodo antes da entrada')
                if elemento != 0: self.FLUXO.at[elemento,'BOP'] = self.FLUXO.at[elemento-1,'EOP']
                self.FLUXO.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']
                
                self.FLUXO.at[elemento,'entrada'] = 0
                self.FLUXO.at[elemento,'reduzida'] = 0
                self.FLUXO.at[elemento,'parcela'] = 0

                self.FLUXO_fake.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO_fake.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']
                
                self.FLUXO_fake.at[elemento,'entrada'] = 0
                self.FLUXO_fake.at[elemento,'reduzida'] = 0
                self.FLUXO_fake.at[elemento,'parcela'] = 0
        
            elif elemento >= qtd_meses_de_diferenca_entre_valor_referencia_e_entrada and elemento < qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas:
                if elemento == 0:  
                    self.FLUXO.at[elemento,'BOP'] = valor_lote
                    self.FLUXO_fake.at[elemento,'BOP'] = valor_lote
                else: 
                    self.FLUXO_fake.at[elemento,'BOP'] = self.FLUXO.at[elemento-1,'EOP']
                if elemento == qtd_meses_de_diferenca_entre_valor_referencia_e_entrada : 
                    self.FLUXO.at[elemento,'juros'] = 0
                    elemento_inicio_entrada = elemento
                else: self.FLUXO.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']
                self.FLUXO_fake.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']

                entrada_minima = self.pd.entrada_minima(percent_valor_entrada,id_emp,valor_lote,0.05)

                self.FLUXO.at[elemento,'entrada'] = (percent_valor_entrada*self.FLUXO.at[elemento_inicio_entrada,'BOP'])/qtd_entradas
                self.FLUXO.at[elemento,'reduzida'] = 0
                self.FLUXO.at[elemento,'parcela'] = 0

                self.FLUXO_fake.at[elemento,'entrada'] = entrada_minima/qtd_entradas
                self.FLUXO_fake.at[elemento,'reduzida'] = 0
                self.FLUXO_fake.at[elemento,'parcela'] = 0

            elif tem_parciais and elemento>= (qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas) and elemento <=  qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas +12:
                self.FLUXO.at[elemento,'BOP'] = self.FLUXO.at[elemento-1,'EOP']
                self.FLUXO.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']

                valor_reduzida = ((self.FLUXO.at[elemento_inicio_entrada,'BOP']-(percent_valor_entrada*self.FLUXO.at[elemento_inicio_entrada,'BOP']))*0.1/12)
                self.FLUXO.at[elemento,'entrada'] = 0
                self.FLUXO.at[elemento,'reduzida'] = valor_reduzida
                self.FLUXO.at[elemento,'parcela'] = 0

                self.FLUXO_fake.at[elemento,'BOP'] = self.FLUXO.at[elemento-1,'EOP']
                self.FLUXO_fake.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO_fake.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']

                valor_reduzida = ((self.FLUXO.at[elemento_inicio_entrada,'BOP']-(percent_valor_entrada*self.FLUXO.at[elemento_inicio_entrada,'BOP']))*0.1/12)
                self.FLUXO_fake.at[elemento,'entrada'] = 0
                self.FLUXO_fake.at[elemento,'reduzida'] = valor_reduzida
                self.FLUXO_fake.at[elemento,'parcela'] = 0

            else:
                self.FLUXO.at[elemento,'BOP'] = self.FLUXO.at[elemento-1,'EOP']
                
                if tem_parciais and elemento == qtd_meses_de_diferenca_entre_valor_referencia_e_entrada+qtd_entradas+12+1 : 
                    elemento_inicio_parcelas = elemento 
                    valor_parcela = (self.FLUXO.at[elemento_inicio_parcelas,'BOP'] * self.juros_amortizacao) / (1 - (1 + self.juros_amortizacao) ** -qtd_parcelas)
                elif elemento == qtd_meses_de_diferenca_entre_valor_referencia_e_entrada+qtd_entradas+1 : 
                    elemento_inicio_parcelas = elemento-1
                    valor_parcela = (self.FLUXO.at[elemento_inicio_parcelas,'BOP'] * self.juros_amortizacao) / (1 - (1 + self.juros_amortizacao) ** -qtd_parcelas)

                self.FLUXO.at[elemento,'juros'] = self.juros_amortizacao * self.FLUXO.at[elemento,'BOP']
                self.FLUXO.at[elemento,'saldoParcial'] = self.FLUXO.at[elemento,'BOP'] + self.FLUXO.at[elemento,'juros']

                self.FLUXO.at[elemento,'entrada'] = 0
                self.FLUXO.at[elemento,'reduzida'] = 0
                self.FLUXO.at[elemento,'parcela'] = valor_parcela

            self.FLUXO.at[elemento,'amortizacao'] = self.FLUXO.at[elemento,'entrada'] + self.FLUXO.at[elemento,'reduzida'] + self.FLUXO.at[elemento,'parcela']
            self.FLUXO.at[elemento,'EOP'] = self.FLUXO.at[elemento,'saldoParcial'] - self.FLUXO.at[elemento,'amortizacao']
        
        return valor_parcela,valor_reduzida,self.FLUXO

    #GERAL
    #Jardim Cristina
    def run_v1(self,valor_lote,percent_valor_entrada,tem_parciais,tem_balao,valor_balao,data_inicio_entrada,data_inicio_balao,data_referencia_juros,qtd_entradas,qtd_parcelas,data_parcela):
        values = {
            'percent':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},
            'valor':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},
            'parcial':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},       
        }

        percent_reduzidas = {
            '3': 0.08771802,
            '2': 0.088551,
            '1': 0.089391,
        }

        values['percent']['entrada'] = percent_valor_entrada

        delta = relativedelta(data_parcela, data_referencia_juros)

        if data_parcela.year == data_referencia_juros.year : delta = data_parcela.month - data_referencia_juros.month
        else: delta = 12 - data_referencia_juros.month +  data_parcela.month 
        # if tem_parciais == False: delta+=1

        qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = delta - qtd_entradas
        print(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)
        if tem_parciais: 
            values['percent']['reduzida'] = percent_reduzidas[str(qtd_entradas)]
            values['percent']['parcela'] = 1 - values['percent']['entrada'] - values['percent']['reduzida']

            values['valor']['entrada'] = valor_lote * values['percent']['entrada'] * (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)
            values['valor']['reduzida'] = valor_lote * values['percent']['reduzida'] * (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada+qtd_entradas-1)
            values['valor']['parcela'] = valor_lote * values['percent']['parcela'] * (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada+qtd_entradas-1+12)
            values['parcial']['entrada'] = values['valor']['entrada']/qtd_entradas
            values['parcial']['reduzida'] = self.pgto(values['valor']['reduzida'],self.juros_amortizacao,12)
            values['parcial']['parcela'] = self.pgto(values['valor']['parcela'],self.juros_amortizacao,qtd_parcelas-12)

        elif tem_balao:
            baloes = {}
            
            ano_primeiro_balao = data_inicio_balao.year
            mes_primeiro_balao = data_inicio_balao.month
            dia_primeiro_balao = data_inicio_balao.days

            ano_balao = ano_primeiro_balao 
            mes_balao = mes_primeiro_balao 
            dia_balao = dia_primeiro_balao 

            baloes[data_inicio_balao] = valor_balao
            
            meses_duracao_financiamento = qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas + qtd_parcelas
            anos_duracao_financiamento = meses_duracao_financiamento/12

            meses_restantes_duracao_financiamento = (anos_duracao_financiamento - math.floor(anos_duracao_financiamento))*30
            
            for ano_adicional in range(0,anos_duracao_financiamento):
                data_balao = dt.date(ano_balao+1,mes_balao,dia_balao)
                baloes[data_balao] = valor_balao
            
            for mes_adicional in range(0,meses_restantes_duracao_financiamento):
                data_balao = dt.date(ano_balao,mes_balao+1,dia_balao)
                if data_balao.month == mes_primeiro_balao:
                    baloes[data_balao] = valor_balao
            
            vp_baloes_totais = self.NPL(data_referencia_juros,baloes)
            n_baloes = len(baloes)
            vp_balao = vp_baloes_totais/n_baloes
            
            saldo_sem_balao = valor_lote - vp_baloes_totais
            saldo_sem_balao_e_sem_entrada = saldo_sem_balao - (percent_valor_entrada * valor_lote)
            valor_parcial_parcela = self.pgto(saldo_sem_balao_e_sem_entrada,self.juros_amortizacao,qtd_parcelas)

            return valor_parcial_parcela,vp_balao,values

        else: 
            values['percent']['reduzida'] = 0
            values['percent']['parcela'] = 1 - values['percent']['entrada'] - values['percent']['reduzida']

            values['valor']['entrada'] = valor_lote * values['percent']['entrada']
            values['valor']['parcela'] = valor_lote * values['percent']['parcela'] * (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada+qtd_entradas-1)

            values['parcial']['entrada'] = values['valor']['entrada']/qtd_entradas
            values['parcial']['parcela'] = self.pgto(values['valor']['parcela'],self.juros_amortizacao,qtd_parcelas)
        
        return values['parcial']['parcela'],values['parcial']['reduzida'],values

    ##Iguaçu
    def run_v2(self,valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela):
        values = {
            'saldo':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},
            'parcial':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},       
        }

        fluxo = {
            '0':{
                'Saldo BOP':0,
                'juros':0,
                'Saldo Parcial':0,
                'Amortizacao':0,
                'Entrada':0,
                'Parcela Reduzida':0,
                'Parcela Excedente':0,
                'Saldo EOP':0
            }
        }

        delta = relativedelta(data_parcela, data_referencia_juros)

        if data_parcela.year == data_referencia_juros.year : delta = data_parcela.month - data_referencia_juros.month
        else: delta = 12 - data_referencia_juros.month +  data_parcela.month 
        # if tem_parciais == False: delta+=1

       

        if tem_parciais: 
            values['saldo']['entrada'] = valor_lote * percent_valor_entrada
            values['parcial']['entrada'] = values['saldo']['entrada']/qtd_entradas
            
            qtd_reduzida = 12

            qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = delta - qtd_entradas - qtd_reduzida

            valor_lote = valor_lote* (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)

            #qtd_entradas
            #qtd_reduzidas
            #qtd_parcelas
            
            tamanho_total_do_fluxo = qtd_entradas + qtd_parcelas
            for mes in range(0,tamanho_total_do_fluxo):

                #se primeiro mês
                if mes == 0:
                    fluxo['0']['Saldo BOP'] = valor_lote
                    fluxo['0']['juros'] = 0
                    fluxo['0']['Saldo Parcial'] = valor_lote 
                
                #se demais meses
                else:
                    fluxo[str(mes)] = {}
                    fluxo[str(mes)]['Saldo BOP'] = fluxo[str(mes-1)]['Saldo EOP']
                    fluxo[str(mes)]['juros'] = fluxo[str(mes)]['Saldo BOP'] * self.juros_amortizacao
                    fluxo[str(mes)]['Saldo Parcial'] = fluxo[str(mes)]['Saldo BOP'] + fluxo[str(mes)]['juros']

                #mes de entrada
                if mes < qtd_entradas:
                    # print('mes',mes,'Entradas')
                    fluxo[str(mes)]['Entrada'] = values['parcial']['entrada']
                    fluxo[str(mes)]['Parcela Reduzida'] = 0
                    fluxo[str(mes)]['Parcela Excedente'] = 0
                    fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                    fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
                
                #mes da primeira reduzida
                if mes == qtd_entradas:
                    valor_reduzida =  (valor_lote * (1-self.pd.entrada_minima(id_emp,valor_lote)/valor_lote) * 0.1,0.05)/12
                    # print('========================================')
                    # print(('valor_reduzida',valor_reduzida,mes,self.pd.entrada_minima(id_emp,valor_lote)/valor_lote), (valor_lote * (1-self.pd.entrada_minima(id_emp,valor_lote)/valor_lote) * 0.1))
                    # print('========================================')

                #mes de reduzida
                if mes >= qtd_entradas and mes < qtd_entradas+12:
                    # print('mes',mes,'Reduzidas')
                    fluxo[str(mes)]['Entrada'] = 0
                    fluxo[str(mes)]['Parcela Reduzida'] = valor_reduzida
                    fluxo[str(mes)]['Parcela Excedente'] = 0
                    fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                    fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']

                #mes da primeira parcela
                if mes == qtd_entradas+12:
                    qtd_parcelas = qtd_parcelas-qtd_reduzida
                    valor_parcela = self.pgto(fluxo[str(mes)]['Saldo BOP'],self.juros_amortizacao,qtd_parcelas)
                    # print('========================================')
                    # print('valor da parcela',valor_parcela,mes,fluxo[str(mes)]['Saldo BOP'],qtd_parcelas)
                    # print('========================================')

                #mes de parcela
                if mes >= qtd_entradas+12:
                    # print('mes',mes,'Parcelas')
                    fluxo[str(mes)]['Entrada'] = 0
                    fluxo[str(mes)]['Parcela Reduzida'] = 0
                    fluxo[str(mes)]['Parcela Excedente'] = valor_parcela
                    fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                    fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
                

        else: 
            qtd_reduzida = 0

            qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = delta - qtd_entradas - qtd_reduzida
            # print(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)

            valor_lote = valor_lote* (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)

            valor_reduzida = 0
            values['saldo']['entrada'] = valor_lote * percent_valor_entrada
            values['parcial']['entrada'] = values['saldo']['entrada']/qtd_entradas

            #qtd_entradas
            #qtd_reduzidas
            #qtd_parcelas
            
            tamanho_total_do_fluxo = qtd_entradas + qtd_parcelas
            for mes in range(0,tamanho_total_do_fluxo):

                #se primeiro mês
                if mes == 0:
                    fluxo['0']['Saldo BOP'] = valor_lote
                    fluxo['0']['juros'] = 0
                    fluxo['0']['Saldo Parcial'] = valor_lote 
                
                #se demais meses
                else:
                    # print('mes',mes,'mes',mes)
                    fluxo[str(mes)] = {}
                    fluxo[str(mes)]['Saldo BOP'] = fluxo[str(mes-1)]['Saldo EOP']
                    fluxo[str(mes)]['juros'] = fluxo[str(mes)]['Saldo BOP'] * self.juros_amortizacao
                    fluxo[str(mes)]['Saldo Parcial'] = fluxo[str(mes)]['Saldo BOP'] + fluxo[str(mes)]['juros']

                #mes de entrada
                if mes < qtd_entradas:
                    # print('mes',mes,'Entradas')
                    fluxo[str(mes)]['Entrada'] = values['parcial']['entrada']
                    fluxo[str(mes)]['Parcela Reduzida'] = 0
                    fluxo[str(mes)]['Parcela Excedente'] = 0
                    fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                    fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
                
                #mes da primeira parcela
                if mes == qtd_entradas:
                    valor_parcela = self.pgto(fluxo[str(mes)]['Saldo BOP'],self.juros_amortizacao,qtd_parcelas)
                    # print('valor da parcela',valor_parcela)

                #mes de parcela
                if mes >= qtd_entradas:
                    # print('mes',mes,'Parcelas')
                    fluxo[str(mes)]['Entrada'] = 0
                    fluxo[str(mes)]['Parcela Reduzida'] = 0
                    fluxo[str(mes)]['Parcela Excedente'] = valor_parcela
                    fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                    fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
        
        
        return valor_parcela,valor_reduzida,fluxo

    def run_v3(self,valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela):
        #Calcula tempo do financimaneto antes do inicio dos pagamentos. Importante para incorrer juros adequadamente
        delta = relativedelta(data_parcela, data_referencia_juros)

        # if data_parcela.year == data_referencia_juros.year : 
        #     print('dentro do mesmo ano')
        #     delta = data_parcela.month - data_referencia_juros.month
        # else: 
        #     print('anos diferentes')
        #     delta = 12 - data_referencia_juros.month +  data_parcela.month 
        
        meses_totais_referencia =  (data_referencia_juros.month+data_referencia_juros.year*12)
        meses_totais_parcela =  (data_parcela.month+data_parcela.year*12)
        delta = meses_totais_parcela - meses_totais_referencia

        # print(delta)
        if data_inicio_entrada.year == data_referencia_juros.year : meses_juros = data_inicio_entrada.month - data_referencia_juros.month
        else: meses_juros = 12 - data_referencia_juros.month +  data_inicio_entrada.month 

        if tem_parciais: qtd_reduzida = 12
        else: qtd_reduzida = 0

        qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = delta - qtd_entradas - qtd_reduzida

        # print(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada,delta)

        mes_de_inicio_das_reduzidas = qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas
        mes_de_inicio_das_parcelas_regulares = qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas + qtd_reduzida 
        # print(mes_de_inicio_das_parcelas_regulares)
        mes_de_fim_do_financiamento = mes_de_inicio_das_parcelas_regulares + qtd_parcelas

        #Aplica correção de juros no periodo de financiamento sem pagamento. REVER SE VAI BATER NA CONTA
        # valor_lote = valor_lote* (1+self.juros_amortizacao)**(qtd_meses_de_diferenca_entre_valor_referencia_e_entrada)

        Fluxo_consolidado = fluxo()
        Fluxo_Entrada = fluxo()
        Fluxo_Reduzidas = fluxo()
        Fluxo_Financiamento = fluxo()
        tamanho_total_do_fluxo = qtd_entradas + qtd_parcelas + qtd_meses_de_diferenca_entre_valor_referencia_e_entrada
        # print(tamanho_total_do_fluxo)

        #corre ao longo do fluxo
        for mes in range(0,tamanho_total_do_fluxo):

            Fluxo_consolidado.df
            Fluxo_Entrada.df
            Fluxo_Reduzidas.df
            Fluxo_Financiamento.df
            ['BOP','juros','saldoParcial','amortizacao','entrada','reduzida','parcela','EOP']

            #Estabelece os BOP no mes zero
            if mes ==0:
                #calcula valor das parcelas reduzidas e vpl do conjunto
                if qtd_reduzida>0:
                    valorReduzida = ((1-0.05)*0.1) * valor_lote/12
                    listFluxo = []
                    # for periodo in range(0,qtd_meses_de_diferenca_entre_valor_referencia_e_entrada):
                    #     listFluxo.append(0)
                    for periodo in range(0,qtd_entradas):
                        listFluxo.append(0)
                    for periodo in range(0,12):
                        listFluxo.append(valorReduzida)
                    # vplReduzida = numpy.npv(self.juros_amortizacao,listFluxo)
                    vplReduzida = self.npv(self.juros_amortizacao,listFluxo)
                else:
                    valorReduzida = 0
                    vplReduzida=0

                #Seta valor de parcela inicialmente como 0
                valorParcela = 0
                # print('antes do bop inicial')

                Fluxo_Entrada.df.at[mes,'BOP'] = valor_lote*percent_valor_entrada
                Fluxo_Entrada.df.at[mes,'juros'] = 0
                Fluxo_Entrada.df.at[mes,'saldoParcial'] = Fluxo_Entrada.df.at[mes,'BOP']+Fluxo_Entrada.df.at[mes,'juros']
                Fluxo_Entrada.df.at[mes,'entrada'] = 0
                Fluxo_Entrada.df.at[mes,'reduzida'] = 0
                Fluxo_Entrada.df.at[mes,'parcela'] = 0
                Fluxo_Entrada.df.at[mes,'amortizacao'] = Fluxo_Entrada.df.at[mes,'entrada']+Fluxo_Entrada.df.at[mes,'reduzida']+Fluxo_Entrada.df.at[mes,'parcela']
                Fluxo_Entrada.df.at[mes,'EOP'] = Fluxo_Entrada.df.at[mes,'saldoParcial'] - Fluxo_Entrada.df.at[mes,'amortizacao']

                if qtd_reduzida>0:
                    Fluxo_Reduzidas.df.at[mes,'BOP'] = ((1-percent_valor_entrada)*0.1) * valor_lote
                    Fluxo_Reduzidas.df.at[mes,'juros'] = 0
                    Fluxo_Reduzidas.df.at[mes,'saldoParcial'] = Fluxo_Reduzidas.df.at[mes,'BOP']+Fluxo_Reduzidas.df.at[mes,'juros']
                    Fluxo_Reduzidas.df.at[mes,'entrada'] = 0
                    Fluxo_Reduzidas.df.at[mes,'reduzida'] = 0
                    Fluxo_Reduzidas.df.at[mes,'parcela'] = 0
                    Fluxo_Reduzidas.df.at[mes,'amortizacao'] = Fluxo_Reduzidas.df.at[mes,'entrada']+Fluxo_Reduzidas.df.at[mes,'reduzida']+Fluxo_Reduzidas.df.at[mes,'parcela']
                    Fluxo_Reduzidas.df.at[mes,'EOP'] = Fluxo_Reduzidas.df.at[mes,'saldoParcial'] - Fluxo_Reduzidas.df.at[mes,'amortizacao']
                else:
                    Fluxo_Reduzidas.df.at[mes,'BOP'] = 0
                    Fluxo_Reduzidas.df.at[mes,'juros'] = 0
                    Fluxo_Reduzidas.df.at[mes,'saldoParcial'] = Fluxo_Reduzidas.df.at[mes,'BOP']+Fluxo_Reduzidas.df.at[mes,'juros']
                    Fluxo_Reduzidas.df.at[mes,'entrada'] = 0
                    Fluxo_Reduzidas.df.at[mes,'reduzida'] = 0
                    Fluxo_Reduzidas.df.at[mes,'parcela'] = 0
                    Fluxo_Reduzidas.df.at[mes,'amortizacao'] = Fluxo_Reduzidas.df.at[mes,'entrada']+Fluxo_Reduzidas.df.at[mes,'reduzida']+Fluxo_Reduzidas.df.at[mes,'parcela']
                    Fluxo_Reduzidas.df.at[mes,'EOP'] = Fluxo_Reduzidas.df.at[mes,'saldoParcial'] - Fluxo_Reduzidas.df.at[mes,'amortizacao']

                Fluxo_Financiamento.df.at[mes,'BOP'] = (1 - percent_valor_entrada - vplReduzida/valor_lote) * valor_lote
                Fluxo_Financiamento.df.at[mes,'juros'] = 0
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'reduzida'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'reduzida']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

                # print(mes,Fluxo_Financiamento.df.at[mes,'BOP'] ,vplReduzida/valor_lote)

                
            #Caso seja um mes depois do primeiro, o BOP será o EOP anterior
            else:
                Fluxo_Entrada.df.at[mes,'BOP'] = Fluxo_Entrada.df.at[mes-1,'EOP']
                Fluxo_Reduzidas.df.at[mes,'BOP'] = Fluxo_Reduzidas.df.at[mes-1,'EOP']
                Fluxo_Financiamento.df.at[mes,'BOP'] = Fluxo_Financiamento.df.at[mes-1,'EOP']

                # print(mes,Fluxo_Financiamento.df.at[mes,'BOP'] )

            #Meses antes do financiamento
            if mes > 0 and mes < qtd_meses_de_diferenca_entre_valor_referencia_e_entrada:
                # print(mes,'- Antes do financiamento')
                
                #acrua juros parcelas recorrentes
                Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'reduzida'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'reduzida']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']
                
            #Meses de entrada
            if  mes >= qtd_meses_de_diferenca_entre_valor_referencia_e_entrada and mes < mes_de_inicio_das_reduzidas:    
                #Amortiza entrada
                Fluxo_Entrada.df.at[mes,'juros'] = 0
                Fluxo_Entrada.df.at[mes,'saldoParcial'] = Fluxo_Entrada.df.at[mes,'BOP']+Fluxo_Entrada.df.at[mes,'juros']
                Fluxo_Entrada.df.at[mes,'entrada'] = valor_lote*percent_valor_entrada/qtd_entradas
                Fluxo_Entrada.df.at[mes,'reduzida'] = 0
                Fluxo_Entrada.df.at[mes,'parcela'] = 0
                Fluxo_Entrada.df.at[mes,'amortizacao'] = Fluxo_Entrada.df.at[mes,'entrada']+Fluxo_Entrada.df.at[mes,'reduzida']+Fluxo_Entrada.df.at[mes,'parcela']
                Fluxo_Entrada.df.at[mes,'EOP'] = Fluxo_Entrada.df.at[mes,'saldoParcial'] - Fluxo_Entrada.df.at[mes,'amortizacao']

                if mes>0:
                    #acrua juros reduzidas
                    if qtd_reduzida>0:
                        Fluxo_Reduzidas.df.at[mes,'juros'] = Fluxo_Reduzidas.df.at[mes,'BOP'] * self.juros_amortizacao
                        Fluxo_Reduzidas.df.at[mes,'saldoParcial'] = Fluxo_Reduzidas.df.at[mes,'BOP']+Fluxo_Reduzidas.df.at[mes,'juros']
                        Fluxo_Reduzidas.df.at[mes,'entrada'] = 0
                        Fluxo_Reduzidas.df.at[mes,'reduzida'] = 0
                        Fluxo_Reduzidas.df.at[mes,'parcela'] = 0
                        Fluxo_Reduzidas.df.at[mes,'amortizacao'] = Fluxo_Reduzidas.df.at[mes,'entrada']+Fluxo_Reduzidas.df.at[mes,'reduzida']+Fluxo_Reduzidas.df.at[mes,'parcela']
                        Fluxo_Reduzidas.df.at[mes,'EOP'] = Fluxo_Reduzidas.df.at[mes,'saldoParcial'] - Fluxo_Reduzidas.df.at[mes,'amortizacao']

                    #acrua juros parcelas recorrentes
                    Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                    Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                    Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                    Fluxo_Financiamento.df.at[mes,'reduzida'] = 0
                    Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                    Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'reduzida']+Fluxo_Financiamento.df.at[mes,'parcela']
                    Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

            #Meses de reduzidas
            if   mes >= mes_de_inicio_das_reduzidas and mes < mes_de_inicio_das_parcelas_regulares:
                if qtd_reduzida>0:
                    Fluxo_Reduzidas.df.at[mes,'juros'] = Fluxo_Reduzidas.df.at[mes,'BOP']  * self.juros_amortizacao
                    Fluxo_Reduzidas.df.at[mes,'saldoParcial'] = Fluxo_Reduzidas.df.at[mes,'BOP']+Fluxo_Reduzidas.df.at[mes,'juros']
                    Fluxo_Reduzidas.df.at[mes,'entrada'] = 0
                    Fluxo_Reduzidas.df.at[mes,'reduzida'] = valorReduzida
                    Fluxo_Reduzidas.df.at[mes,'parcela'] = 0
                    Fluxo_Reduzidas.df.at[mes,'amortizacao'] = Fluxo_Reduzidas.df.at[mes,'entrada']+Fluxo_Reduzidas.df.at[mes,'reduzida']+Fluxo_Reduzidas.df.at[mes,'parcela']
                    Fluxo_Reduzidas.df.at[mes,'EOP'] = Fluxo_Reduzidas.df.at[mes,'saldoParcial'] - Fluxo_Reduzidas.df.at[mes,'amortizacao']

                #acrua juros parcelas recorrentes
                Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'reduzida'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'reduzida']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

            #Meses de parcelas regulares
            # print('-------------------------------------')
            # print(mes , qtd_meses_de_diferenca_entre_valor_referencia_e_entrada , qtd_entradas , qtd_reduzida,mes >= qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas + qtd_reduzida )
            # print(mes , tamanho_total_do_fluxo,mes < tamanho_total_do_fluxo)
            
            if mes >= mes_de_inicio_das_parcelas_regulares and mes < tamanho_total_do_fluxo:  
                
                if valorParcela == 0: 
                    # print(mes,'====================================')
                    valorParcela = self.pgto(Fluxo_Financiamento.df.at[mes,'BOP'],self.juros_amortizacao,qtd_parcelas-qtd_reduzida)
                    # print(Fluxo_Financiamento.df.at[mes,'BOP'],self.juros_amortizacao,qtd_parcelas-qtd_reduzida,valorParcela)

                # print(mes,'- Parcelas regulares',Fluxo_Financiamento.df.at[mes,'BOP'])
                Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'reduzida'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = valorParcela
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'reduzida']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

            # print('----------------------------------------------------------------------------')
            # print(mes)
            # print(Fluxo_Financiamento.df.loc[mes,:])
        if tem_parciais: valor_reduzida_sem_juros = self.calcula_valor_reduzida_sem_juros(valorReduzida,qtd_entradas)
        else: valor_reduzida_sem_juros = 0
        valorReduzida = self.corrige_valor_reduzida_com_juros(valorReduzida,qtd_entradas,meses_juros)

        # print(round(Fluxo_Financiamento.df.at[mes,'EOP'],2),Fluxo_Financiamento.df.at[mes,'EOP'])
        if round(Fluxo_Financiamento.df.at[mes,'EOP'],2) == 0:
            return valorParcela,valorReduzida,Fluxo_Financiamento,valor_reduzida_sem_juros
        else:
            return 0,0,0,0

    def run_24x_sem_juros(self,valor_lote,percent_valor_entrada,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela):
        
        values = {
            'saldo':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},
            'parcial':{
                'entrada':0,
                'reduzida':0,
                'parcela':0},       
        }

        fluxo = {
            '0':{
                'Saldo BOP':0,
                'juros':0,
                'Saldo Parcial':0,
                'Amortizacao':0,
                'Entrada':0,
                'Parcela Reduzida':0,
                'Parcela Excedente':0,
                'Saldo EOP':0
            }
        }

        valor_reduzida = 0
        values['saldo']['entrada'] = valor_lote * percent_valor_entrada
        values['parcial']['entrada'] = values['saldo']['entrada']/qtd_entradas

        tamanho_total_do_fluxo = qtd_entradas + qtd_parcelas

        for mes in range(0,tamanho_total_do_fluxo):

            #se primeiro mês
            if mes == 0:
                fluxo['0']['Saldo BOP'] = valor_lote
                fluxo['0']['juros'] = 0
                fluxo['0']['Saldo Parcial'] = valor_lote 
            
            #se demais meses
            else:
                # print('mes',mes,'mes',mes)
                fluxo[str(mes)] = {}
                fluxo[str(mes)]['Saldo BOP'] = fluxo[str(mes-1)]['Saldo EOP']
                fluxo[str(mes)]['juros'] = fluxo[str(mes)]['Saldo BOP'] * self.juros_amortizacao
                fluxo[str(mes)]['Saldo Parcial'] = fluxo[str(mes)]['Saldo BOP'] + fluxo[str(mes)]['juros']

            #mes de entrada
            if mes < qtd_entradas:
                # print('mes',mes,'Entradas')
                fluxo[str(mes)]['Entrada'] = values['parcial']['entrada']
                fluxo[str(mes)]['Parcela Reduzida'] = 0
                fluxo[str(mes)]['Parcela Excedente'] = 0
                fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
            
            #mes da primeira parcela
            if mes == qtd_entradas:
                valor_parcela = fluxo[str(mes)]['Saldo BOP']/qtd_parcelas
                # print('valor da parcela',valor_parcela)

            #mes de parcela
            if mes >= qtd_entradas:
                # print('mes',mes,'Parcelas')
                fluxo[str(mes)]['Entrada'] = 0
                fluxo[str(mes)]['Parcela Reduzida'] = 0
                fluxo[str(mes)]['Parcela Excedente'] = valor_parcela
                fluxo[str(mes)]['Amortizacao'] = fluxo[str(mes)]['Entrada'] + fluxo[str(mes)]['Parcela Reduzida'] + fluxo[str(mes)]['Parcela Excedente']
                fluxo[str(mes)]['Saldo EOP'] = fluxo[str(mes)]['Saldo Parcial'] - fluxo[str(mes)]['Amortizacao']
        
        return valor_parcela,valor_reduzida,fluxo

    def NPL(cashflows,data_inicial):
        tx = ((1.12)**(1/12))-1
        total = 0.0
        for data in cashflows:
            mes = round(((data-data_inicial).days)/30,0)
            total += cashflows[data]/(1+tx)**mes
        return total

    def run_balao(self,valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entradas,qtd_parcelas,id_emp,data_parcela,valor_balao,data_inicio_balao):
        values = {
            'percent':{
                'entrada':0,
                'balao':0,
                'parcela':0},
            'valor':{
                'entrada':0,
                'balao':0,
                'parcela':0},     
        }

        #Calcula tempo do financimaneto antes do inicio dos pagamentos. Importante para incorrer juros adequadamente
        delta = relativedelta(data_parcela, data_referencia_juros)
        
        meses_totais_referencia =  (data_referencia_juros.month+data_referencia_juros.year*12)
        meses_totais_parcela =  (data_parcela.month+data_parcela.year*12)
        delta = meses_totais_parcela - meses_totais_referencia

        if data_inicio_entrada.year == data_referencia_juros.year : meses_juros = data_inicio_entrada.month - data_referencia_juros.month
        else: meses_juros = 12 - data_referencia_juros.month +  data_inicio_entrada.month 


        qtd_meses_de_diferenca_entre_valor_referencia_e_entrada = delta - qtd_entradas

        mes_de_inicio_das_parcelas_regulares = qtd_meses_de_diferenca_entre_valor_referencia_e_entrada + qtd_entradas 
        mes_de_fim_do_financiamento = mes_de_inicio_das_parcelas_regulares + qtd_parcelas


        #Define os fluxos
        Fluxo_consolidado = fluxo()
        Fluxo_Entrada = fluxo()
        Fluxo_balao = fluxo()
        Fluxo_Financiamento = fluxo()
        tamanho_total_do_fluxo = qtd_entradas + qtd_parcelas + qtd_meses_de_diferenca_entre_valor_referencia_e_entrada

        #Cria fluxo de balão
        # mes_inicio = dt.date(data_referencia_juros.year,(mes_de_inicio_das_parcelas_regulares+data_referencia_juros.month),data_referencia_juros.day).month
        # mes_inicio = data_referencia_juros+relativedelta(months=+mes_de_inicio_das_parcelas_regulares).month
        # ano_inicio = dt.date(data_referencia_juros.year,(mes_de_inicio_das_parcelas_regulares+data_referencia_juros.month),data_referencia_juros.day).year
        # ano_inicio = data_referencia_juros+relativedelta(months=+mes_de_inicio_das_parcelas_regulares).year
        
        mes_balao = data_inicio_balao.month

        numero_mes_do_primeiro_balao = (data_inicio_balao.month+data_inicio_balao.year*12) - (data_referencia_juros.month+data_referencia_juros.year*12)

        mes = 0
        mes_observado = data_referencia_juros

        fluxo_balao = []
        qtd_baloes = 0
        
        while mes < tamanho_total_do_fluxo:

            if mes == 0:fluxo_balao.append(0)

            else:
                if mes_observado.month == mes_balao:
                    fluxo_balao.append(valor_balao)
                    qtd_baloes += 1
                else:
                    fluxo_balao.append(0)
                
            mes_observado = mes_observado+relativedelta(months=+1)

            # if mes_observado.month+1>12: mes_observado = dt.date(mes_observado.year+1,1,1)
            # else: mes_observado = dt.date(mes_observado.year,mes_observado.month+1,1)
            mes += 1
        
        #calcula os subtotais das series
        # vpl_balao = numpy.npv(self.juros_amortizacao,fluxo_balao)
        vpl_balao = self.npv(self.juros_amortizacao,fluxo_balao)
        total_entrada = percent_valor_entrada * valor_lote
        total_parcelas = valor_lote - total_entrada - vpl_balao
        parcelaSemJuros = total_parcelas/qtd_parcelas

        

        if str(id_emp) not in self.parcelasMinimasComBalao:
            return [False, 'Este empreendimento nao permite balões.','']
        if parcelaSemJuros < self.parcelasMinimasComBalao[str(id_emp)] :
            texto = '''Valor da parcela mensal está muito baixa!

O valor atual é de %s reais.

Reduza o valor do balão para não ser superior a 5 vezes do valor de parcela.'''%(round(parcelaSemJuros,2))
            print(texto)
            return [False, texto,'','','']

        print(fluxo_balao)
        print('quantidade de baloes',qtd_baloes)
        print('valor_balao',valor_balao)
        print('vpl_balao',vpl_balao)
        print('total_entrada',total_entrada)
        print('total_parcelas',total_parcelas)

        values['percent']['balao'] = vpl_balao/valor_lote
        values['percent']['parcela'] = total_parcelas/valor_lote

        #calcula valor da parcela
        # valorParcela = self.pgto(total_parcelas,self.juros_amortizacao,qtd_parcelas) 
        # print('valor_parcela',valorParcela)

        #corre ao longo do fluxo
        for mes in range(0,tamanho_total_do_fluxo):

            Fluxo_consolidado.df
            Fluxo_Entrada.df
            Fluxo_balao.df
            Fluxo_Financiamento.df
            ['BOP','juros','saldoParcial','amortizacao','entrada','parcela','EOP']

            #Estabelece os BOP no mes zero
            if mes == 0:

                #Seta valor de parcela inicialmente como 0
                Fluxo_Entrada.df.at[mes,'BOP'] = valor_lote*percent_valor_entrada
                Fluxo_Entrada.df.at[mes,'juros'] = 0
                Fluxo_Entrada.df.at[mes,'saldoParcial'] = Fluxo_Entrada.df.at[mes,'BOP']+Fluxo_Entrada.df.at[mes,'juros']
                Fluxo_Entrada.df.at[mes,'entrada'] = 0
                Fluxo_Entrada.df.at[mes,'balao'] = 0
                Fluxo_Entrada.df.at[mes,'parcela'] = 0
                Fluxo_Entrada.df.at[mes,'amortizacao'] = Fluxo_Entrada.df.at[mes,'entrada']+Fluxo_Entrada.df.at[mes,'balao']+Fluxo_Entrada.df.at[mes,'parcela']
                Fluxo_Entrada.df.at[mes,'EOP'] = Fluxo_Entrada.df.at[mes,'saldoParcial'] - Fluxo_Entrada.df.at[mes,'amortizacao']

                Fluxo_balao.df.at[mes,'BOP'] = values['percent']['balao'] * valor_lote
                Fluxo_balao.df.at[mes,'juros'] = 0
                Fluxo_balao.df.at[mes,'saldoParcial'] = Fluxo_balao.df.at[mes,'BOP']+Fluxo_balao.df.at[mes,'juros']
                Fluxo_balao.df.at[mes,'entrada'] = 0
                Fluxo_balao.df.at[mes,'balao'] = 0
                Fluxo_balao.df.at[mes,'parcela'] = 0
                Fluxo_balao.df.at[mes,'amortizacao'] = Fluxo_balao.df.at[mes,'entrada']+Fluxo_balao.df.at[mes,'balao']+Fluxo_balao.df.at[mes,'parcela']
                Fluxo_balao.df.at[mes,'EOP'] = Fluxo_balao.df.at[mes,'saldoParcial'] - Fluxo_balao.df.at[mes,'amortizacao']

                Fluxo_Financiamento.df.at[mes,'BOP'] = (values['percent']['parcela']) * valor_lote
                Fluxo_Financiamento.df.at[mes,'juros'] = 0
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'balao'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'balao']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']
            
            #Caso seja um mes depois do primeiro, o BOP será o EOP anterior
            else:
                Fluxo_Entrada.df.at[mes,'BOP'] = Fluxo_Entrada.df.at[mes-1,'EOP']
                Fluxo_balao.df.at[mes,'BOP'] = Fluxo_balao.df.at[mes-1,'EOP']
                Fluxo_Financiamento.df.at[mes,'BOP'] = Fluxo_Financiamento.df.at[mes-1,'EOP']
                # print(mes,Fluxo_Financiamento.df.at[mes,'BOP'] )

            #Meses antes do financiamento
            if mes > 0 and mes < qtd_meses_de_diferenca_entre_valor_referencia_e_entrada:
                # print(mes,'- Antes do financiamento')
                
                #acrua juros parcelas recorrentes
                Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'balao'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'balao']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']
                
            #Meses de entrada
            if  mes >= qtd_meses_de_diferenca_entre_valor_referencia_e_entrada and mes < mes_de_inicio_das_parcelas_regulares:    
                # print(mes,'- Mes da entrada')
                #Amortiza entrada
                Fluxo_Entrada.df.at[mes,'juros'] = 0
                Fluxo_Entrada.df.at[mes,'saldoParcial'] = Fluxo_Entrada.df.at[mes,'BOP']+Fluxo_Entrada.df.at[mes,'juros']
                Fluxo_Entrada.df.at[mes,'entrada'] = valor_lote*percent_valor_entrada/qtd_entradas
                Fluxo_Entrada.df.at[mes,'balao'] = 0
                Fluxo_Entrada.df.at[mes,'parcela'] = 0
                Fluxo_Entrada.df.at[mes,'amortizacao'] = Fluxo_Entrada.df.at[mes,'entrada']+Fluxo_Entrada.df.at[mes,'balao']+Fluxo_Entrada.df.at[mes,'parcela']
                Fluxo_Entrada.df.at[mes,'EOP'] = Fluxo_Entrada.df.at[mes,'saldoParcial'] - Fluxo_Entrada.df.at[mes,'amortizacao']

                if mes>0:
                    #acrua juros parcelas recorrentes
                    Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                    Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                    Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                    Fluxo_Financiamento.df.at[mes,'balao'] = 0
                    Fluxo_Financiamento.df.at[mes,'parcela'] = 0
                    Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'balao']+Fluxo_Financiamento.df.at[mes,'parcela']
                    Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

            #Meses de balão
            if (mes == numero_mes_do_primeiro_balao or (mes - numero_mes_do_primeiro_balao)%12 == 0) and mes < tamanho_total_do_fluxo:
                # print(mes,'- Mes de balao')

                Fluxo_balao.df.at[mes,'juros'] = Fluxo_balao.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_balao.df.at[mes,'saldoParcial'] = Fluxo_balao.df.at[mes,'BOP']+Fluxo_balao.df.at[mes,'juros']
                Fluxo_balao.df.at[mes,'entrada'] = 0
                Fluxo_balao.df.at[mes,'balao'] = valor_balao
                Fluxo_balao.df.at[mes,'parcela'] = 0
                Fluxo_balao.df.at[mes,'amortizacao'] = Fluxo_balao.df.at[mes,'entrada']+Fluxo_balao.df.at[mes,'balao']+Fluxo_balao.df.at[mes,'parcela']
                Fluxo_balao.df.at[mes,'EOP'] = Fluxo_balao.df.at[mes,'saldoParcial'] - Fluxo_balao.df.at[mes,'amortizacao']
            
            else:
                Fluxo_balao.df.at[mes,'juros'] = Fluxo_balao.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_balao.df.at[mes,'saldoParcial'] = Fluxo_balao.df.at[mes,'BOP']+Fluxo_balao.df.at[mes,'juros']
                Fluxo_balao.df.at[mes,'entrada'] = 0
                Fluxo_balao.df.at[mes,'balao'] = 0
                Fluxo_balao.df.at[mes,'parcela'] = 0
                Fluxo_balao.df.at[mes,'amortizacao'] = Fluxo_balao.df.at[mes,'entrada']+Fluxo_balao.df.at[mes,'balao']+Fluxo_balao.df.at[mes,'parcela']
                Fluxo_balao.df.at[mes,'EOP'] = Fluxo_balao.df.at[mes,'saldoParcial'] - Fluxo_balao.df.at[mes,'amortizacao']


            #Meses de parcelas regulares            
            if mes >= mes_de_inicio_das_parcelas_regulares and mes < tamanho_total_do_fluxo: 

                if mes == mes_de_inicio_das_parcelas_regulares:
                    valorParcela = self.pgto(Fluxo_Financiamento.df.at[mes,'BOP'],self.juros_amortizacao,qtd_parcelas) 
                    print('valor_parcela',Fluxo_Financiamento.df.at[mes,'BOP'])

                Fluxo_Financiamento.df.at[mes,'juros'] = Fluxo_Financiamento.df.at[mes,'BOP']  * self.juros_amortizacao
                Fluxo_Financiamento.df.at[mes,'saldoParcial'] = Fluxo_Financiamento.df.at[mes,'BOP']+Fluxo_Financiamento.df.at[mes,'juros']
                Fluxo_Financiamento.df.at[mes,'entrada'] = 0
                Fluxo_Financiamento.df.at[mes,'balao'] = 0
                Fluxo_Financiamento.df.at[mes,'parcela'] = valorParcela
                Fluxo_Financiamento.df.at[mes,'amortizacao'] = Fluxo_Financiamento.df.at[mes,'entrada']+Fluxo_Financiamento.df.at[mes,'parcela']
                Fluxo_Financiamento.df.at[mes,'EOP'] = Fluxo_Financiamento.df.at[mes,'saldoParcial'] - Fluxo_Financiamento.df.at[mes,'amortizacao']

        # print(Fluxo_Entrada.df)
        # print(Fluxo_Financiamento.df)
        # print(Fluxo_balao.df)


        if round(Fluxo_Financiamento.df.at[mes,'EOP'],2) == 0:
            valorReduzida = 0
            valor_reduzida_sem_juros = 0 
            
            # valor_balao_sem_juros = self.calcula_valor_balao_sem_juros(Fluxo_balao.df,qtd_baloes)
            valor_balao_sem_juros =vpl_balao/qtd_baloes

            if parcelaSemJuros*5 < valor_balao_sem_juros :
                texto = '''Valor da parcela mensal está muito baixa!

    O valor atual é de %s reais.

    Reduza o valor do balão para não ser superior a 5 vezes do valor de parcela.'''%(round(parcelaSemJuros,2))
                print(texto)
                return [False, texto,'','','']

            return valorParcela,valor_balao,Fluxo_Financiamento,qtd_baloes,valor_balao_sem_juros
        else:
            return 0,0,0,0,0



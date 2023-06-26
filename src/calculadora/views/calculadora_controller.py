
from flask_classful import FlaskView, route
from flask import request
import datetime as dt
from dateutil.relativedelta import *
from flask import Response
import jsonify

# from src.autenticacao.service.credenciamento_service import autenticacao
from src.calculadora.services.calculadora_services import prep_dados,fluxo,main
# from src.dados_cliente.service.contratos_de_cliente_service import capta_dados_de_contratos_de_cliente,trata_dados_de_contratos_de_cliente


class calculadora_view(FlaskView):
    route_base = '/calculadora/'

    @route('/parcelas', methods=['POST'])
    def resumo_cliente(self):

        try:
            body = (request.get_json())

            # id_empreendimento = int(body.get('id_empreendimento'))
            id_empreendimento = '1'
            valor_lote = float(body.get('valor_lote'))
            data_referencia_juros = dt.datetime.today()
            
            valor_entrada = float(body.get('valor_entrada'))
            qtd_entrada = int(body.get('qtd_entrada'))
            data_inicio_entrada = body.get('data_inicio_entrada')
            percent_valor_entrada = valor_entrada/valor_lote
            
            qtd_parcelas = int(body.get('qtd_parcelas'))
            data_inicio_parcelas = body.get('data_inicio_parcela')
            
            try:
                tem_balao = body.get('tem_balao')
                if str(tem_balao).lower() == 'true': tem_balao = True
                if str(tem_balao).lower() == 'false': tem_balao = False
            except:
                tem_balao = False
            valor_balao = body.get('valor_balao')
            data_inicio_balao = body.get('data_inicio_balao')
            if tem_balao:
                valor_balao = float(valor_balao)
            
            # try:
            #     tem_parciais = body.get('tem_parciais')
            #     if str(tem_parciais).lower() == 'true': tem_parciais = True
            #     if str(tem_parciais).lower() == 'false': tem_parciais = False
            # except:
            #     tem_parciais = False
            tem_parciais = False

            
            
        except Exception as e:
            print(str(e))
            return {"status":404,"message":'Revise os dados imputados'} 


        print('===========================================================')
        print("REQUISIÇÃO DE CALCULADORA DE PARCELAS")
        print('===========================================================')

        try:
            # auth = autenticacao()
            prepara_dados = prep_dados()
            calculo = main()
        except Exception as e:
            print(str(e))
            {"status":500,"message":'Serviço fora do ar'}

        try:
            data_inicio_entrada = prepara_dados.str_to_date(data_inicio_entrada)
            data_inicio_parcelas = prepara_dados.str_to_date(data_inicio_parcelas)
            if tem_balao: data_inicio_balao = prepara_dados.str_to_date(data_inicio_balao)
            data_inicio_entrada_limite_parcela = dt.date(data_inicio_entrada.year,data_inicio_entrada.month+1,data_inicio_entrada.day)

            if qtd_parcelas > 240:
                return {"status":404,"message":"Mais parcelas mensais do que o permitido (240x)"}

            if valor_entrada < valor_lote/10:
                return {"status":404,"message":"Entrada menor do que o mínimo permitido (%s)"%(valor_lote/10)}
            
            if qtd_entrada > 5:
                return {"status":404,"message":"Mais parcelas de entrada do que o permitido (5x)"}
            
            if data_inicio_parcelas < data_inicio_entrada:
                return {"status":404,"message":"A data de vencimento das parcelas mensais não pode ser anter da data de vencimento da entrada"}
            
            if tem_balao and data_inicio_balao < data_inicio_entrada:
                return {"status":404,"message":"A data de vencimento dos balões não pode ser anter da data de vencimento da entrada"}
            
            if data_inicio_parcelas > data_inicio_entrada_limite_parcela:
                return {"status":404,"message":"A data de vencimento das parcelas mensais não pode ser mais do que 1 mes depois da data de vencimento da entrada"}

            print('calculando valores')
            if tem_parciais: 
                data_inicio_parciais = data_inicio_parcelas
                data_inicio_parcelas = data_inicio_parciais + relativedelta(months=+12)
            else:
                data_inicio_parciais = 0

            # response_validation = prepara_dados.valida_datas(data_inicio_entrada,qtd_entrada,data_inicio_parciais,data_inicio_parcelas)
            # print(response_validation)
            # if response_validation[0] == False:
            #     retorno = {'status':'404','message':response_validation[1]}
            #     return retorno
            # else:
            #     print('Data ok!')

  
            valor_parcela,valor_reduzida,valores_totais,valor_reduzida_sem_juros,entrada_minima,qtd_balao,valor_balao_sem_juros = calculo.run_all(valor_lote,percent_valor_entrada,tem_parciais,data_inicio_entrada,data_referencia_juros,qtd_entrada,qtd_parcelas,id_empreendimento,data_inicio_parcelas,data_inicio_parciais,tem_balao,valor_balao,data_inicio_balao)

            #Erro no calculo
            if valor_parcela == False:
                treated_data = {
                        'status':404,
                        'message':valor_reduzida, 
                    }
                return treated_data

        except Exception as e:
            print('Erro ->',str(e))
            return '404 - Calculo falhou!!'

        response = prepara_dados.trata_retorno(valor_parcela,valor_reduzida,entrada_minima*valor_lote,valor_entrada,tem_parciais,tem_balao,valor_reduzida_sem_juros,qtd_balao,valor_balao_sem_juros)

        # response = prepara_dados.trata_retorno(0,0,0*0,0,0,0,0,0,0)
        print(response[0])
        return response[1]





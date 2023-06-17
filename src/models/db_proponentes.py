from src import db
from sqlalchemy import Column, Integer, String

class Proponentes(db.Model):
    __tablename__= "proponentes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    estado_civil = db.Column(db.String(50), nullable=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    filhos = db.Column(db.Float, nullable=False)
    renda_familiar = db.Column(db.Float, nullable=False)
    entrada = db.Column(db.Float, nullable=False)
    num_parcelas = db.Column(db.Float, nullable=False)
    divida = db.Column(db.Float, nullable=False)
    valor_lote = db.Column(db.Float, nullable=False)
    valor_parcela = db.Column(db.Float, nullable=False)
    moradia_atual = db.Column(db.String(50), nullable=False)
    tempo_clt = db.Column(db.String(50), nullable=False)
    comprou_pra_morar = db.Column(db.String(50), nullable=False)
    moradores = db.Column(db.String(50), nullable=False)
    aprovado_1_analise = db.Column(db.String(50), nullable=False)
    aprovado_2_analise = db.Column(db.String(50), nullable=False)
    aprovado_final = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.String(50), nullable=False)
    empreendimentos = db.Column(db.String(50), nullable=False)
    data_analise = db.Column(db.DateTime, nullable=False)
    porcentagem_renda = db.Column(db.Float, nullable=False)
    porcentagem_divida = db.Column(db.Float, nullable=False)
    idade_fim_financiamento = db.Column(db.Float, nullable=False)
    data_proposta = db.Column(db.DateTime, nullable=False)
    profissao = db.Column(db.String(50), nullable=False)
    profissao_formal = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.DateTime, nullable=False)
    comprovante = db.Column(db.String(50), nullable=False)
    num_entrada = db.Column(db.Float, nullable=False)
    cliente = db.Column(db.String(50), nullable=False)
    soma_parcela = db.Column(db.Float, nullable=False)
    porcentagem_final = db.Column(db.Float, nullable=False)
    versao_bru = db.Column(db.String(50), nullable=False)
    porcentagem_bru_1_0 = db.Column(db.String(50), nullable=False)
    porcentagem_bru_1_5 = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id': self.id,
            'nome': self.nome,
            'documento': self.documento,
            'data_nascimento': self.data_nascimento,
            'estado_civil': self.estado_civil,
            'escolaridade': self.escolaridade,
            'filhos': self.filhos,
            'renda_familiar': self.renda_familiar,
            'entrada': self.entrada,
            'num_parcelas': self.num_parcelas,
            'divida': self.divida,
            'valor_lote': self.valor_lote,
            'valor_parcela': self.valor_parcela,
            'moradia_atual': self.moradia_atual,
            'tempo_clt': self.tempo_clt,
            'comprou_pra_morar': self.comprou_pra_morar,
            'moradores': self.moradores,
            'aprovado_1_analise': self.aprovado_1_analise,
            'aprovado_2_analise': self.aprovado_2_analise,
            'aprovado_final': self.aprovado_final,
            'observacao': self.observacao,
            'empreendimentos': self.empreendimentos,
            'data_analise': self.data_analise,
            'porcentagem_renda': self.porcentagem_renda,
            'porcentagem_divida': self.porcentagem_divida,
            'idade_fim_financiamento': self.idade_fim_financiamento,
            'data_proposta': self.data_proposta,
            'profissao': self.profissao,
            'profissao_formal': self.profissao_formal,
            'data_admissao': self.data_admissao,
            'comprovante': self.comprovante,
            'num_entrada': self.num_entrada,
            'cliente': self.cliente,
            'soma_parcela': self.soma_parcela,
            'porcentagem_final': self.porcentagem_final,
            'versao_bru': self.versao_bru,
            'porcentagem_bru_1_0': self.porcentagem_bru_1_0,
            'porcentagem_bru_1_5': self.porcentagem_bru_1_5, 
        }

        return str(self.package)


    # def __repr__(self):
    #     return "id_contrato='%s'| documento='%s'| nome='%s'| nome_empreendimento='%s'| lote='%s'| quadra='%s'|codigo_cliente = '%s'|sexo = '%s'|estado_civil = '%s'|data_nascimento = '%s'|tipo = '%s'|endereco = '%s'|data_contrato = '%s'|area = '%s'|data_status = '%s'|codigo_empreendimento = '%s'|inadimplente = '%s'|imobiliaria = '%s'|ltv = '%s'|matricula = '%s'|nacionalidade = '%s'|numero_aditivos = '%s'|rg = '%s'|nome_spe = '%s'|status = '%s'|telefone = '%s'|tier = '%s'|valor_contrato = '%s'|valor_entrada = '%s'|valor_pago_parcelas = '%s'|data_atualizacao = '%s'|valor_encargos = '%s'|valor_iptu = '%s'|codigo_unidade = '%s'|id_emp = '%s'|cep = '%s'|score = '%s'" % (self.id_contrato, self.documento, self.nome, self.nome_empreendimento, self.lote, self.quadra,self.codigo_cliente,self.sexo,self.estado_civil,self.data_nascimento,self.tipo,self.endereco,self.data_contrato,self.area,self.data_status,self.codigo_empreendimento,self.inadimplente,self.imobiliaria,self.ltv,self.matricula,self.nacionalidade,self.numero_aditivos,self.rg,self.nome_spe,self.status,self.telefone,self.tier,self.valor_contrato,self.valor_entrada,self.valor_pago_parcelas,self.data_atualizacao,self.valor_encargos,self.valor_iptu,self.codigo_unidade,self.id_emp,self.cep,self.score)



from src import db
from sqlalchemy import Column, Integer, String

class Enterprises(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "enterprises"
    id = db.Column(db.String(50) ,primary_key=True)
    name = db.Column(db.String(50) ,nullable=False)
    cnpj = db.Column(db.String(50) ,nullable=False)
    empresa = db.Column(db.String(50) ,nullable=False)
    razao_social = db.Column(db.String(50) ,nullable=False)
    uf = db.Column(db.String(50) ,nullable=False)
    cidade = db.Column(db.String(50) ,nullable=False)
    bairro = db.Column(db.String(50) ,nullable=False)
    cep = db.Column(db.String(50) ,nullable=False)
    logradouro = db.Column(db.String(50) ,nullable=False)
    cod_empreendimento = db.Column(db.Integer ,nullable=False)
    cod_filial = db.Column(db.Integer ,nullable=False)
    lotes_totais = db.Column(db.Integer ,nullable=False)
    lotes_disponiveis = db.Column(db.Integer ,nullable=False)
    created_at = db.Column(db.DateTime ,nullable=False)
    updated_at = db.Column(db.DateTime ,nullable=False)
    foto_implantacao = db.Column(db.String(50) ,nullable=False)
    quantidade_parcelas = db.Column(db.Integer ,nullable=False)
    quantidade_maxima_entradas = db.Column(db.Integer ,nullable=False)
    valor_minimo_entrada = db.Column(db.Float ,nullable=False)
    tipo_loteamento = db.Column(db.String(50) ,nullable=False)
    totalmente_vendido = db.Column(db.Boolean, nullable=False)
    status_empreendimento = db.Column(db.String(50) ,nullable=False)
    destaque = db.Column(db.Boolean, nullable=False)
    parcela_minima_reduzidas = db.Column(db.Float ,nullable=False)
    parcela_minima_normal = db.Column(db.Float ,nullable=False)
    parcela_minima_updated_date = db.Column(db.DateTime ,nullable=False)
    regiao = db.Column(db.String(50) ,nullable=False)
    area_minima_lote = db.Column(db.Float ,nullable=False)
    area_maxima_lote = db.Column(db.Float ,nullable=False)
    valor_minimo_lote = db.Column(db.Float ,nullable=False)
    valor_maximo_lote = db.Column(db.Float ,nullable=False)


    def __repr__(self):
        self.package  = {
            'id':self.id,
            'name':self.name,
            'cnpj':self.cnpj,
            'empresa':self.empresa,
            'razao_social':self.razao_social,
            'uf':self.uf,
            'cidade':self.cidade,
            'bairro':self.bairro,
            'cep':self.cep,
            'logradouro':self.logradouro,
            'cod_empreendimento':self.cod_empreendimento,
            'cod_filial':self.cod_filial,
            'lotes_totais':self.lotes_totais,
            'lotes_disponiveis':self.lotes_disponiveis,
            'foto_implantacao':self.foto_implantacao,
            'quantidade_parcelas':self.quantidade_parcelas,
            'quantidade_maxima_entradas':self.quantidade_maxima_entradas,
            'valor_minimo_entrada':self.valor_minimo_entrada,
            'tipo_loteamento':self.tipo_loteamento,
            'totalmente_vendido':self.totalmente_vendido,
            'status_empreendimento':self.status_empreendimento,
            'destaque':self.destaque,
            'parcela_minima_reduzidas':self.parcela_minima_reduzidas,
            'parcela_minima_normal':self.parcela_minima_normal,
            'parcela_minima_updated_date':self.parcela_minima_updated_date.strftime("%Y-%m-%d"),
            'regiao':self.regiao,
            'area_minima_lote':self.area_minima_lote,
            'area_maxima_lote':self.area_maxima_lote,
            'valor_minimo_lote':self.valor_minimo_lote,
            'valor_maximo_lote':self.valor_maximo_lote,
            'created_at':self.created_at.strftime("%Y-%m-%d"),
            'updated_at':self.updated_at.strftime("%Y-%m-%d")
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
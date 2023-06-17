from src import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

class PropostasFisicas(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "proposals_physical"
    id =db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estado_civil = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    num_filhos = db.Column(db.Integer, nullable=False)
    renda_familiar = db.Column(db.String(50), nullable=False)
    num_entradas = db.Column(db.Integer, nullable=False) 
    valor_entrada = db.Column(db.Float, nullable=False)
    valor_parcelas = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    objetivo = db.Column(db.String(50), nullable=False)
    num_parcelas = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    land_id = db.Column(db.Integer, nullable=False)
    proposta_enviada = db.Column(db.Boolean, nullable=False)
    comentary = db.Column(db.String(50), nullable=False)
    moradia_atual = db.Column(db.String(50), nullable=False)
    numero_pessoas_morar = db.Column(db.Integer, nullable=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    clt = db.Column(db.String(50), nullable=False)
    data_vencimento_sinal = db.Column(db.DateTime, nullable=False)
    data_vencimento_parcela = db.Column(db.DateTime, nullable=False)
    data_vencimento_reduzidas = db.Column(db.DateTime, nullable=False)
    valor_reduzidas = db.Column(db.Integer, nullable=False)
    quadra_lote = db.Column(db.String(50), nullable=False)
    cod_mega_proposta_ativa = db.Column(db.Integer, nullable=False)
    sale_occured = db.Column(db.Boolean, nullable=False)
    id_pipe = db.Column(db.Integer, nullable=False)

    

    def __repr__(self):
        self.package  = {
            'id':self.id,
            'estado_civil':self.estado_civil,
            'data_nascimento':self.data_nascimento,
            'num_filhos':self.num_filhos,
            'renda_familiar':self.renda_familiar,
            'num_entradas':self.num_entradas,
            'valor_entrada':self.valor_entrada,
            'valor_parcelas':self.valor_parcelas,
            'valor_total':self.valor_total,
            'status':self.status,
            'objetivo':self.objetivo,
            'num_parcelas':self.num_parcelas,
            'id_user':self.id_user,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'land_id':self.land_id,
            'proposta_enviada':self.proposta_enviada,
            'comentary':self.comentary,
            'moradia_atual':self.moradia_atual,
            'numero_pessoas_morar':self.numero_pessoas_morar,
            'escolaridade':self.escolaridade,
            'clt':self.clt,
            'data_vencimento_sinal':self.data_vencimento_sinal,
            'data_vencimento_parcela':self.data_vencimento_parcela,
            'data_vencimento_reduzidas':self.data_vencimento_reduzidas,
            'valor_reduzidas':self.valor_reduzidas,
            'quadra_lote':self.quadra_lote,
            'cod_mega_proposta_ativa':self.cod_mega_proposta_ativa,
            'sale_occured':self.sale_occured,
            'id_pipe':self.id_pipe
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)




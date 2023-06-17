from src import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

class LeadActions(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "leads_actions"
    id =db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_lead =db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    id_user = db.Column(db.String(50), nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    land_id = db.Column(db.Float, nullable=False)
    pontuacao = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        self.package  = {
            'id':self.id,
            'id_lead':self.id_lead,
            'id_user':self.id_user,
            'acao':self.acao,
            'land_id':self.land_id,
            'pontuacao':self.pontuacao,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
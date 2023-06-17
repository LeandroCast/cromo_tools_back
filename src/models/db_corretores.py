from src import db
from sqlalchemy import Column, Integer, String
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Corretores(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    document = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    avatar = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    agency_id = db.Column(UUID(as_uuid=True),default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    points=db.Column(db.Integer, primary_key=False)
    proposals_number=db.Column(db.Integer, primary_key=False)
    sales_number=db.Column(db.Integer, primary_key=False)
    creci = db.Column(db.DateTime, nullable=False)
    firebase_token = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        self.package  = {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'password':self.password,
            'document':self.document,
            'birth_date':self.birth_date,
            'avatar':self.avatar,
            'phone':self.phone,
            'user_type':self.user_type,
            'agency_id':self.agency_id,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'points':self.points,
            'proposals_number':self.proposals_number,
            'sales_number':self.sales_number,
            'creci':self.creci,
            'firebase_token':self.firebase_token
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)



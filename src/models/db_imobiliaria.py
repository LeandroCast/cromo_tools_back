from src import db
from sqlalchemy import Column, Integer, String
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Imobiliaria(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "agencies"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(50), nullable=False)
    telefone=db.Column(db.Integer, primary_key=False)
    email = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(50), nullable=False)
    razao_social = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(50), nullable=False)
    logradouro = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    creci = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id':self.id,
            'nome':self.nome,
            'telefone':self.telefone,
            'email':self.email,
            'cnpj':self.cnpj,
            'razao_social':self.razao_social,
            'cep':self.cep,
            'logradouro':self.logradouro,
            'uf':self.uf,
            'cidade':self.cidade,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'creci':self.creci,
            'bairro':self.bairro,
            'numero':self.numero
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
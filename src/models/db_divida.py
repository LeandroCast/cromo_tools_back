from src import db
from sqlalchemy import Column, Integer, String

class Divida(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "divida"
    id =db.Column(db.Integer, primary_key=True)
    tecnospeed_serasa_token = db.Column(db.String(50), nullable=False)
    proposal_id = db.Column(db.String(50), nullable=False)
    quod_score = db.Column(db.Float, nullable=False)
    renda_presumida = db.Column(db.Float, nullable=False)
    divida_total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    cpf = db.Column(db.String(50), nullable=False)
    exato_token = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id':self.id,
            'tecnospeed_serasa_token':self.tecnospeed_serasa_token,
            'proposal_id':self.proposal_id,
            'quod_score':self.quod_score,
            'renda_presumida':self.renda_presumida,
            'divida_total':self.divida_total,
            'created_at':self.created_at.strftime("%Y-%m-%d"),
            'updated_at':self.updated_at.strftime("%Y-%m-%d"),
            'cpf':self.cpf,
            'exato_token':self.exato_token
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
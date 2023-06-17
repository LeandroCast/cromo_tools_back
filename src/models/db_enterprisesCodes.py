from src import db
from sqlalchemy import Column, Integer, String
import uuid
from sqlalchemy.dialects.postgresql import UUID

class EnterprisesCodes(db.Model):
    __bind_key__ = 'gc'
    __tablename__= "enterprises_codes"
    enterprise_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enterprise_code = db.Column(db.Integer ,nullable=False)


    def __repr__(self):
        self.package  = {
            'enterprise_id':self.enterprise_id,
            'enterprise_code':self.enterprise_code
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
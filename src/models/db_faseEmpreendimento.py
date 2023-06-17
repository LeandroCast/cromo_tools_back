from src import db
from sqlalchemy import Column, Integer, String

class FaseEmpreendimento(db.Model):
    __tablename__= "fase_empreendimento"
    id_fase = db.Column(db.String(50), primary_key=True)
    id_emp = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    comissao = db.Column(db.String(50), nullable=False)
    lotes = db.Column(db.String(50), nullable=False)
    nome_comercial = db.Column(db.String(50), nullable=False)
    nome_mega = db.Column(db.String(50), nullable=False)
    data_lancamento = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id_fase':self.id_fase,
            'id_emp':self.id_emp,
            'codigo':self.codigo,
            'comissao':self.comissao,
            'lotes':self.lotes,
            'nome_comercial':self.nome_comercial,
            'nome_mega':self.nome_mega,
            'data_lancamento':self.data_lancamento,
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
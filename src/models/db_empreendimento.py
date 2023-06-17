from src import db
from sqlalchemy import Column, Integer, String

class Empreendimentos(db.Model):
    __tablename__= "empreendimentos"
    id_emp = db.Column(db.String(50), primary_key=True)
    bairro = db.Column(db.String(50), nullable=False)
    cartorio = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(50), nullable=False)
    contratos_ativos = db.Column(db.String(50), nullable=False)
    endereco_catorio = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    filial = db.Column(db.Integer,  nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    nome_spe = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    parcela_media = db.Column(db.Float,  nullable=False)
    rua = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(50), nullable=False)
    controle_comissao = db.Column(db.Boolean, nullable=False)
    seguradora = db.Column(db.String(50), nullable=False)
    atraso_em_porc_pc = db.Column(db.Float,  nullable=False)
    origem = db.Column(db.String(50), nullable=False)
    cod_banco = db.Column(db.Integer,  nullable=False)
    agencia = db.Column(db.Integer,  nullable=False)
    conta = db.Column(db.Integer,  nullable=False)


    def __repr__(self):
        self.package  = {
            'id_emp' : self.id_emp,
            'bairro' : self.bairro,
            'cartorio' : self.cartorio,
            'cep' : self.cep,
            'cnpj' : self.cnpj,
            'contratos_ativos' : int(self.contratos_ativos),
            'endereco_catorio' : self.endereco_catorio,
            'endereco' : self.endereco,
            'filial' : int(self.filial),
            'municipio' : self.municipio,
            'nome' : self.nome,
            'nome_spe' : self.nome_spe,
            'pais' : self.pais,
            'parcela_media' : self.parcela_media,
            'rua' : self.rua,
            'tipo' : self.tipo,
            'uf' : self.uf,
            'controle_comissao' : self.controle_comissao,
            'seguradora' : self.seguradora,
            'atraso_em_porc_pc' : self.atraso_em_porc_pc,
            'origem' : self.origem,
            'cod_banco' : self.cod_banco,
            'agencia' : self.agencia,
            'conta' : self.conta,
        }

        return str(self.package)

    # def __repr__(self):
    #     return "id_emp='%s' | bairro='%s' | cartorio='%s' | cep='%s' | cnpj='%s' | contratos_ativos='%s' | endereco_catorio='%s' | endereco='%s' | filial='%s' | municipio='%s' | nome='%s' | nome_spe='%s' | pais='%s' | parcela_media='%s' | rua='%s' | tipo='%s' | uf='%s' | controle_comissao='%s' | seguradora='%s' | atraso_em_porc_pc='%s' | origem='%s' | cod_banco='%s' | agencia='%s' | conta='%s'" % (self.id_emp, self.bairro, self.cartorio, self.cep, self.cnpj, self.contratos_ativos, self.endereco_catorio, self.endereco, self.filial, self.municipio, self.nome, self.nome_spe, self.pais, self.parcela_media, self.rua, self.tipo, self.uf, self.controle_comissao, self.seguradora, self.atraso_em_porc_pc, self.origem, self.cod_banco, self.agencia, self.conta)


 
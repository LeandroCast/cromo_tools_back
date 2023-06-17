from src import db
from sqlalchemy import Column, Integer, String

class Clientes(db.Model):
    __tablename__= "clientes"
    id_contrato = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    nome_empreendimento = db.Column(db.String(50), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    quadra = db.Column(db.String(50), nullable=False)
    codigo_cliente = db.Column(db.Integer,  nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    estado_civil = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    data_contrato = db.Column(db.DateTime, nullable=False)
    area = db.Column(db.Float, nullable=False)
    data_status = db.Column(db.DateTime, nullable=False)
    codigo_empreendimento = db.Column(db.Integer,  nullable=False)
    inadimplente = db.Column(db.Boolean, nullable=False)
    imobiliaria = db.Column(db.String(50), nullable=False)
    ltv = db.Column(db.Float, nullable=False)
    matricula = db.Column(db.String(50),  nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    numero_aditivos = db.Column(db.Integer, nullable=False)
    rg = db.Column(db.String(50), nullable=False)
    nome_spe = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    tier = db.Column(db.String(50), nullable=False)
    valor_contrato = db.Column(db.Float, nullable=False)
    valor_entrada = db.Column(db.Float, nullable=False)
    valor_pago_parcelas = db.Column(db.Float, nullable=False)
    data_atualizacao = db.Column(db.DateTime, nullable=False)
    valor_encargos = db.Column(db.Float, nullable=False)
    valor_iptu = db.Column(db.Float, nullable=False)
    codigo_unidade = db.Column(db.Integer,  nullable=False)
    id_emp = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __repr__(self):
        self.package  = {
            'id_contrato' : str(int(self.id_contrato)),
            'documento' : str(self.documento),
            'nome' : self.nome,
            'nome_empreendimento' : self.nome_empreendimento,
            'lote' : self.lote,
            'quadra' : self.quadra,
            'codigo_cliente' : int(self.codigo_cliente),
            'sexo' : self.sexo,
            'estado_civil' : self.estado_civil,
            'data_nascimento' : str(self.data_nascimento),
            'tipo' : self.tipo,
            'endereco' : self.endereco,
            'data_contrato' : str(self.data_contrato),
            'area' : self.area,
            'data_status' : str(self.data_status),
            'codigo_empreendimento' : str(int(self.codigo_empreendimento)),
            'inadimplente' : self.inadimplente,
            'imobiliaria' : self.imobiliaria,
            'ltv' : self.ltv,
            'matricula' : str(self.matricula),
            'nacionalidade' : self.nacionalidade,
            'numero_aditivos' : str(int(self.numero_aditivos)),
            'rg' : self.rg,
            'nome_spe' : self.nome_spe,
            'status' : self.status,
            'telefone' : self.telefone,
            'tier' : self.tier,
            'valor_contrato' : self.valor_contrato,
            'valor_entrada' : self.valor_entrada,
            'valor_pago_parcelas' : self.valor_pago_parcelas,
            'data_atualizacao' : str(self.data_atualizacao),
            'valor_encargos' : self.valor_encargos,
            'valor_iptu' : self.valor_iptu,
            'codigo_unidade' : str(int(self.codigo_unidade)),
            'id_emp' : self.id_emp,
            'cep' : self.cep,
            'score' : self.score
        }

        return str(self.package)


    # def __repr__(self):
    #     return "id_contrato='%s'| documento='%s'| nome='%s'| nome_empreendimento='%s'| lote='%s'| quadra='%s'|codigo_cliente = '%s'|sexo = '%s'|estado_civil = '%s'|data_nascimento = '%s'|tipo = '%s'|endereco = '%s'|data_contrato = '%s'|area = '%s'|data_status = '%s'|codigo_empreendimento = '%s'|inadimplente = '%s'|imobiliaria = '%s'|ltv = '%s'|matricula = '%s'|nacionalidade = '%s'|numero_aditivos = '%s'|rg = '%s'|nome_spe = '%s'|status = '%s'|telefone = '%s'|tier = '%s'|valor_contrato = '%s'|valor_entrada = '%s'|valor_pago_parcelas = '%s'|data_atualizacao = '%s'|valor_encargos = '%s'|valor_iptu = '%s'|codigo_unidade = '%s'|id_emp = '%s'|cep = '%s'|score = '%s'" % (self.id_contrato, self.documento, self.nome, self.nome_empreendimento, self.lote, self.quadra,self.codigo_cliente,self.sexo,self.estado_civil,self.data_nascimento,self.tipo,self.endereco,self.data_contrato,self.area,self.data_status,self.codigo_empreendimento,self.inadimplente,self.imobiliaria,self.ltv,self.matricula,self.nacionalidade,self.numero_aditivos,self.rg,self.nome_spe,self.status,self.telefone,self.tier,self.valor_contrato,self.valor_entrada,self.valor_pago_parcelas,self.data_atualizacao,self.valor_encargos,self.valor_iptu,self.codigo_unidade,self.id_emp,self.cep,self.score)


from src import db
from sqlalchemy import Column, Integer, String

class Clientes_simplificado(db.Model):
    __tablename__= "clientes"
    id_contrato = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    nome_empreendimento = db.Column(db.String(50), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    quadra = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id_contrato' : int(self.id_contrato),
            'nome' : self.nome,
            'nome_empreendimento' : self.nome_empreendimento,
            'lote' : self.lote,
            'quadra' : self.quadra,
            'status' : self.status,
        }

        return str(self.package)


    # def __repr__(self):
    #     return "id_contrato='%s'| documento='%s'| nome='%s'| nome_empreendimento='%s'| lote='%s'| quadra='%s'|codigo_cliente = '%s'|sexo = '%s'|estado_civil = '%s'|data_nascimento = '%s'|tipo = '%s'|endereco = '%s'|data_contrato = '%s'|area = '%s'|data_status = '%s'|codigo_empreendimento = '%s'|inadimplente = '%s'|imobiliaria = '%s'|ltv = '%s'|matricula = '%s'|nacionalidade = '%s'|numero_aditivos = '%s'|rg = '%s'|nome_spe = '%s'|status = '%s'|telefone = '%s'|tier = '%s'|valor_contrato = '%s'|valor_entrada = '%s'|valor_pago_parcelas = '%s'|data_atualizacao = '%s'|valor_encargos = '%s'|valor_iptu = '%s'|codigo_unidade = '%s'|id_emp = '%s'|cep = '%s'|score = '%s'" % (self.id_contrato, self.documento, self.nome, self.nome_empreendimento, self.lote, self.quadra,self.codigo_cliente,self.sexo,self.estado_civil,self.data_nascimento,self.tipo,self.endereco,self.data_contrato,self.area,self.data_status,self.codigo_empreendimento,self.inadimplente,self.imobiliaria,self.ltv,self.matricula,self.nacionalidade,self.numero_aditivos,self.rg,self.nome_spe,self.status,self.telefone,self.tier,self.valor_contrato,self.valor_entrada,self.valor_pago_parcelas,self.data_atualizacao,self.valor_encargos,self.valor_iptu,self.codigo_unidade,self.id_emp,self.cep,self.score)

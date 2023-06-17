from src import db
from sqlalchemy import Column, Integer, String

class Parcelas(db.Model):
    __tablename__= "parcelas"
    id_parcela = db.Column(db.Integer, primary_key=True)
    id_contrato = db.Column(db.Integer, nullable=False)
    sequencia = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    valor_presente = db.Column(db.Float, nullable=False)
    vencimento = db.Column(db.DateTime, nullable=False)
    pagamento = db.Column(db.DateTime, nullable=False)
    dias_atraso = db.Column(db.Integer,  nullable=False)
    encargos = db.Column(db.Float, nullable=False)
    descontos = db.Column(db.Float, nullable=False)
    tipo_inflacao = db.Column(db.String(50), nullable=False)
    valor_original = db.Column(db.Float, nullable=False)
    classifica_parcela = db.Column(db.String(50), nullable=False)
    nosso_numero = db.Column(db.String(50), nullable=False)
    valor_adiantamento = db.Column(db.Float, nullable=False)
    valor_corrigido = db.Column(db.Float, nullable=False)
    data_vigencia = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        self.package  = {
            'id_parcela' : int(self.id_parcela),
            'id_contrato' : int(self.id_contrato),
            'sequencia' : self.sequencia,
            'tipo' : self.tipo,
            'status' : self.status,
            'valor' : self.valor,
            'valor_pago' : self.valor_pago,
            'valor_presente' : self.valor_presente,
            'vencimento' : str(self.vencimento),
            'pagamento' : str(self.pagamento),
            'dias_atraso' : int(self.dias_atraso),
            'encargos' : self.encargos,
            'descontos' : self.descontos,
            'tipo_inflacao' : self.tipo_inflacao,
            'valor_original' : self.valor_original,
            'classifica_parcela' : self.classifica_parcela,
            'nosso_numero' : self.nosso_numero,
            'valor_adiantamento' : self.valor_adiantamento,
            'valor_corrigido' : self.valor_corrigido,
            'data_vigencia' : str(self.data_vigencia)
        }

        return str(self.package)


    # def __repr__(self):
    #     return "|id_parcela='%s'|id_contrato='%s'|sequencia='%s'|tipo='%s'|status='%s'|valor='%s'|valor_pago='%s'|valor_presente='%s'|vencimento='%s'|pagamento='%s'|dias_atraso='%s'|encargos='%s'|descontos='%s'|tipo_inflacao='%s'|valor_original='%s'|classifica_parcela='%s'|nosso_numero='%s'|valor_adiantamento='%s'|valor_corrigido='%s'|data_vigencia='%s'" % (self.id_parcela,self.id_contrato,self.sequencia,self.tipo,self.status,self.valor,self.valor_pago,self.valor_presente,self.vencimento,self.pagamento,self.dias_atraso,self.encargos,self.descontos,self.tipo_inflacao,self.valor_original,self.classifica_parcela,self.nosso_numero,self.valor_adiantamento,self.valor_corrigido,self.data_vigencia)

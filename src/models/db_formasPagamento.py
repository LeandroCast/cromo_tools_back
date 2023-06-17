from src import db
from sqlalchemy import Column, Integer, String
import json
import os
import json
from dotenv import load_dotenv, find_dotenv
from itertools import groupby
from datetime import datetime
import requests as req
import uuid
from sqlalchemy.dialects.postgresql import UUID

class FormasPagamentos(db.Model):
    
    __bind_key__ = 'gc'
    __tablename__= "codigo_forma_pagamento"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_empreendimento = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    codigo_forma_pagamento = db.Column(db.Integer, nullable=False)
    entrada_minima = db.Column(db.Float, nullable=False)
    quantidade_max_parcelas_entrada = db.Column(db.Integer, nullable=False)
    quantidade_max_parcelas_mensal = db.Column(db.Integer, nullable=False)
    reduzidas  = db.Column(db.Boolean, nullable=False)
    curto_sem_juros = db.Column(db.Boolean, nullable=False)
    baloes = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        self.package  = {
            'id':str(self.id),
            'id_empreendimento':str(self.id_empreendimento),
            'codigo_forma_pagamento':str(self.codigo_forma_pagamento),
            'entrada_minima':str(self.entrada_minima),
            'quantidade_max_parcelas_entrada':str(self.quantidade_max_parcelas_entrada),
            'quantidade_max_parcelas_mensal':str(self.quantidade_max_parcelas_mensal),
            'reduzidas':str(self.reduzidas),
            'curto_sem_juros':str(self.curto_sem_juros),
            'baloes':str(self.baloes)
        }
        return str(self.package)

        # return req.Response(json.dumps(self.package),  mimetype="application/json")
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)





from src import db
from sqlalchemy import Column, Integer, String
import json
import os
import json
from dotenv import load_dotenv, find_dotenv
from itertools import groupby
from datetime import datetime
import requests as req

class Lotes(db.Model):
    __tablename__= "lotes"
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer, nullable=False)
    cod_emp = db.Column(db.Integer, nullable=False)
    empreendimento = db.Column(db.String(50), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    proposta_ativa = db.Column(db.Integer, nullable=False)
    quadra  = db.Column(db.String(50), nullable=False)
    status_atual = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor_atual = db.Column(db.Float, nullable=False)
    recompensa = db.Column(db.String(50), nullable=False)
    latitude  = db.Column(db.Float, nullable=False)
    longitude  = db.Column(db.Float, nullable=False)
    empreendimento_plataforma = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id':int(self.id),
            'area':int(self.area),
            'cod_emp':int(self.cod_emp),
            'empreendimento':self.empreendimento,
            'lote':self.lote,
            'proposta_ativa':self.proposta_ativa,
            'quadra':self.quadra,
            'status_atual':self.status_atual,
            'tipo':self.tipo,
            'valor_atual':self.valor_atual,
            'recompensa':self.recompensa,
            'latitude':self.latitude,
            'longitude':self.longitude,
            'empreendimento_plataforma':self.empreendimento_plataforma
        }
        retorno = json.dumps(self.package)
        # return req.Response(json.dumps(self.package),  content_type="application/json")
        # return req.Response(retorno,  mimetype="application/json")
        return retorno
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)





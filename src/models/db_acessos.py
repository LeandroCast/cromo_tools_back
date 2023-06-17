from src import db
from sqlalchemy import Column, Integer, String
import json
import os
import json
from dotenv import load_dotenv, find_dotenv
from itertools import groupby
from datetime import datetime
import requests as req

class Acessos(db.Model):
    __tablename__= "acessos_api_tech"
    id_acesso = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(50), nullable=False)
    requisicao = db.Column(db.String(50), nullable=False)
    data_req = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        self.package  = {
            'id_acesso' : int(self.id_acesso),
            'usuario' : self.usuario,
            'token' : self.token,
            'requisicao' : self.requisicao,
            'data_req' : str(self.data_req),
        }

        return req.Response(json.dumps(self.package),  mimetype="application/json")
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)




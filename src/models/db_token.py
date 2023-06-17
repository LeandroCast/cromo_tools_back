import mimetypes
from src import db
from sqlalchemy import Column, Integer, String
from flask import jsonify

class Token(db.Model):
    __tablename__= "token_api_tech"

    token  = db.Column(db.String(50), primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    data_geracao = db.Column(db.DateTime, nullable=False)

    def cria_json(self):
        self.package  = {
            'token' : self.token ,
            'usuario':self.usuario,
            'data_geracao' : self.data_geracao
        }

    def __repr__(self):
        self.cria_json()
        return str(self.package)
        # return response = self.package, status = 200, mimetype=json

    # def __repr__(self):
    #     return "token='%s'| data_geracao='%s'" % (self.token, self.data_geracao)
        # return "token='%s'| data_geracao='%s'| id_user='%s'" % (self.token, self.data_geracao, self.id_user)

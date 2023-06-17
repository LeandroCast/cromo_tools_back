from src import db
from sqlalchemy import Column, Integer, String
import json
import os
import json
from dotenv import load_dotenv, find_dotenv
from itertools import groupby
from datetime import datetime
import requests as req


class Credenciais(db.Model):
    __tablename__= "credenciais_api_tech"
    id_user = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        self.package  = {
            'id_user' : self.id_user,
            'password' : self.password,
            'data_criacao' : str(self.data_criacao)
        }

        return str(self.package)
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)




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

class Coordenadas(db.Model):
    
    __bind_key__ = 'gc'
    __tablename__= "enterprise_coordinates"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_empreendimento = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    lat_canto_inf_esq_mapa = db.Column(db.Float, nullable=False)
    lat_canto_sup_dir_mapa = db.Column(db.Float, nullable=False)
    long_canto_sup_dir_mapa = db.Column(db.Float, nullable=False)
    long_canto_inf_esq_mapa = db.Column(db.Float, nullable=False)
    lat_centro_mapa  = db.Column(db.Float, nullable=False)
    long_centro_mapa = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        self.package  = {
            'id':self.id,
            'id_empreendimento':self.id_empreendimento,
            'lat_canto_inf_esq_mapa':self.lat_canto_inf_esq_mapa,
            'lat_canto_sup_dir_mapa':self.lat_canto_sup_dir_mapa,
            'long_canto_sup_dir_mapa':self.long_canto_sup_dir_mapa,
            'long_canto_inf_esq_mapa':self.long_canto_inf_esq_mapa,
            'lat_centro_mapa':self.lat_centro_mapa,
            'long_centro_mapa':self.long_centro_mapa,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(self.package)

        # return req.Response(json.dumps(self.package),  mimetype="application/json")
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)





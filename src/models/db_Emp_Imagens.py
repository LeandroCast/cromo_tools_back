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

class Imagens(db.Model):
    
    __bind_key__ = 'gc'
    __tablename__= "enterprise_images"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_empreendimento = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    url = db.Column(db.String(50), nullable=False)
    principal = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        self.package  = {
            'id':self.id,
            'id_empreendimento':self.id_empreendimento,
            'url':self.url,
            'principal':self.principal,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(self.package)

        # return req.Response(json.dumps(self.package),  mimetype="application/json")
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)





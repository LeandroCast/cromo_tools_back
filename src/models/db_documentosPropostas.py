# from ctypes.wintypes import tagMSG
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

class Documentos(db.Model):
    
    __bind_key__ = 'gc'
    __tablename__= "proposals_physical_documents"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    document = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    proposal_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)

    def __repr__(self):
        self.package  = {
            'id':str(self.id),
            'participant_id':str(self.participant_id),
            'document':str(self.document),
            'tag':str(self.tag),
            'proposal_id':str(self.proposal_id),
        }
        return str(self.package)

        # return req.Response(json.dumps(self.package),  mimetype="application/json")
    
    # def __repr__(self):
    #     return "id_user='%s'| password='%s'| data_criacao='%s'" % (self.id_user, self.password, self.data_criacao)





from datetime import datetime
from typing import Optional
from fastapi import HTTPException,status
# from fastapi.encoders import jsonable_encoder

from sqlalchemy import and_, or_


from sqlalchemy.orm import Session
from core.security import verify_password,get_password_hash
from crud.base import CRUDBase

from models import Usuario
# from schemas import PistaAuditoria


class CRUDUsuario(CRUDBase[Usuario]):

    def get(self, db: Session, id: str):
        return db.query(Usuario).filter(Usuario.id == id).first()

    def create_usuario(self, db: Session, *, obj_in: Usuario):

        obj_in.usu_password  = get_password_hash(obj_in.usu_password)
        
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

usuario = CRUDUsuario(Usuario)


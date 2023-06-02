from datetime import datetime
from typing import Optional
from fastapi import HTTPException,status
# from fastapi.encoders import jsonable_encoder

from sqlalchemy import and_, or_
from api import deps

from sqlalchemy.orm import Session
from core.security import verify_password,get_password_hash
from crud.base import CRUDBase

from models import Usuario
# from schemas import PistaAuditoria


class CRUDUsuario(CRUDBase[Usuario]):

    def get(self, db: Session, id: str):
        return db.query(Usuario).filter(Usuario.id == id).first()

    def get_usuario(self,db:Session,*,usu_email:str):
        
        return db.query(Usuario).filter(Usuario.usu_email.__eq__(usu_email)).first()   


    def login(self, db: Session, *, email:str,password:str):

        usuarioDB = self.get_usuario(db=db,usu_email=email)
        if not verify_password(deps.desencriptar_base64(password), usuarioDB.usu_password):
            return None
        
        return usuarioDB

    
    def create_usuario(self, db: Session, *, obj_in: Usuario):

        usuarioDB = self.get_usuario(db=db,usu_email=deps.encriptar(obj_in.usu_email))
        
        if usuarioDB == None:
            obj_in.usu_password  = get_password_hash(obj_in.usu_password)
            obj_in.usu_nombre    = deps.encriptar(obj_in.usu_nombre) 
            obj_in.usu_apellido  = deps.encriptar(obj_in.usu_apellido) 
            obj_in.usu_genero    = deps.encriptar(obj_in.usu_genero) 
            obj_in.usu_pais      = deps.encriptar(obj_in.usu_pais) 
            obj_in.usu_edad      = deps.encriptar(obj_in.usu_edad) 
            obj_in.usu_provincia = deps.encriptar(obj_in.usu_provincia) 
            obj_in.usu_canton    = deps.encriptar(obj_in.usu_canton) 
            obj_in.usu_parroquia = deps.encriptar(obj_in.usu_parroquia) 
            obj_in.usu_street1   = deps.encriptar(obj_in.usu_street1) 
            obj_in.usu_street2   = deps.encriptar(obj_in.usu_street2) 
            obj_in.usu_phone     = deps.encriptar(obj_in.usu_phone) 
            obj_in.usu_phonehome = deps.encriptar(obj_in.usu_phonehome) 
            obj_in.usu_numhome   = deps.encriptar(obj_in.usu_numhome) 
            obj_in.usu_email     = deps.encriptar(obj_in.usu_email) 

            db.add(obj_in)
            db.commit()
            db.refresh(obj_in)
            
            return obj_in
    
    def get_usuario_id(self, db: Session, id: int):
        return db.query(Usuario.usu_path).filter(Usuario.usu_id == id).first()

usuario = CRUDUsuario(Usuario)


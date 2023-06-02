import crud , models,schemas
from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Any
import json
from api import deps
from core import security
from core.config import settings
from pydantic import BaseModel
import base64
from ..feature_extraction import extrart_features
# Tyhy5gKCu1M1rSgt
# url: str = "https://eifkdjviahuhlnkjjijr.supabase.co"
# key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpZmtkanZpYWh1aGxua2pqaWpyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODU1OTQzNjEsImV4cCI6MjAwMTE3MDM2MX0.Sc67LOi5EqpFchUYjNot6l0SxHN9tHZzmmHJ8YW9LVk"
# supabase: Client = create_client(url, key)

router = APIRouter()

class Datos(BaseModel):
    
    data : str 
    

class AuthVerificate(BaseModel):
    usu_id : str 
    photoHand : str 

@router.post("/access-token")
def login_access_token(
    db: Session = Depends(deps.get_db), 
     form_data: OAuth2PasswordRequestForm = Depends()
)-> Any:
    
    resp = crud.usuario.login(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )
    
    if resp != None:
        print(resp.__dict__)
        return {"msg": "true","usuario":resp}
    else:
        return {"msg": "false","usuario":""}



@router.post("/create-user")
def create_user(
    body:Datos,
    db:Session = Depends(deps.get_db),
)->any:
    
    contenido_cifrado = base64.b64decode(body.data)
    contenido_desencriptado = bytearray()

    for i in range(len(contenido_cifrado)):
        byte_desencriptado = contenido_cifrado[i] ^ ord(settings.SECRET_KEY[i % len(settings.SECRET_KEY)])
        contenido_desencriptado.append(byte_desencriptado)

    texto_desencriptado = contenido_desencriptado.decode('utf-8')
    data_json = json.loads(texto_desencriptado)

    usuarioSchema = schemas.Usuario(**data_json)
    usuario = models.Usuario(**jsonable_encoder(usuarioSchema))
    resp = crud.usuario.create_usuario(db=db,obj_in=usuario)

    if resp == None:
        return {"msg": "true"}
    else:
        return {"msg": "false"}


@router.post("/send-auth")
def send_auth(
    body:AuthVerificate,
    db:Session = Depends(deps.get_db),
)->any:
    
    print(
        body
    )

    model_path = crud.usuario.get_usuario_id(
        db=db,
        id=body.usu_id
    )

    model_prediction = extrart_features(body.photoHand,model_path)

    if model_prediction:
        return {"msg": "true"}
    else:
        return {"msg": "false"}
    

    # print(jsonable_encoder())\
""" 

 """
"""     print(usuario.__dict__)
    
    resp = crud.usuario.create_usuario(db=db,obj_in=usuario)
    
    print(resp.__dict__) """


    # user = crud.usuario.authenticate(
    #     db, username=form_data.username, password=form_data.password
    # )
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")

    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # return {
    #     "access_token": security.create_access_token(
    #         user.usu_codigo,expires_delta=access_token_expires
    #     ),
    #     "token_type": "bearer"
    # }


import crud , models
from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from typing import Any

from api import deps
from core import security
from core.config import settings
from pydantic import BaseModel

# Tyhy5gKCu1M1rSgt
# url: str = "https://eifkdjviahuhlnkjjijr.supabase.co"
# key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpZmtkanZpYWh1aGxua2pqaWpyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODU1OTQzNjEsImV4cCI6MjAwMTE3MDM2MX0.Sc67LOi5EqpFchUYjNot6l0SxHN9tHZzmmHJ8YW9LVk"
# supabase: Client = create_client(url, key)

router = APIRouter()

class Datos(BaseModel):
    
    data : str 

@router.post("/access-token")
def login_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
)-> Any:


    print(form_data.username)
    print(form_data.password)

    user = crud.usuario.get_all(db)
    print(user)

@router.post("/create-user")
def create_user(
    body:Datos,
    db:Session = Depends(deps.get_db),
)->any:
    print(body.data)
""" 
    usuario = models.Usuario(
        usu_name ="",
        usu_lastname ="",
        usu_country ="",
        usu_province ="",
        usu_canton ="",
        usu_parish ="",
        usu_street1 ="",
        usu_street2 ="",
        usu_phone ="",
        usu_phonehome ="",
        usu_numhome ="",
        usu_email    = deps.desencriptar(form_data.username),
        usu_password = deps.desencriptar(form_data.password)
    )
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


# import schemas , models

from typing import Any, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core import security
from core.config import settings
from db.session import SessionLocal
import base64

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db()-> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



def encriptar(texto):
    contenido_encriptado = bytearray()

    for i in range(len(texto)):
        byte_cifrado = ord(texto[i]) ^ ord(settings.SECRET_KEY[i % len(settings.SECRET_KEY)])
        contenido_encriptado.append(byte_cifrado)

    contenido_encriptado_base64 = base64.b64encode(contenido_encriptado)
    return contenido_encriptado_base64.decode("utf-8")

def desencriptar_base64(texto):
    contenido_encriptado = base64.b64decode(texto)

    contenido_desencriptado = bytearray()
    for i in range(len(contenido_encriptado)):
        byte_desencriptado = contenido_encriptado[i] ^ ord(settings.SECRET_KEY[i % len(settings.SECRET_KEY)])
        contenido_desencriptado.append(byte_desencriptado)

    return contenido_desencriptado.decode("utf-8")
""" 
def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(reusable_oauth2)
)-> models.Usuario:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.usuario.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.Usuario = Depends(get_current_user),
):
    if not crud.usuario.is_active(current_user) == "A":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user """

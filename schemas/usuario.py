from typing import List, Optional
from pydantic import BaseModel, EmailStr,SecretStr

class UsuarioBase(BaseModel):

    usu_nombre    : Optional[str]
    usu_apellido  : Optional[str]
    usu_genero    : Optional[str]
    usu_pais      : Optional[str]
    usu_edad      : Optional[str]
    usu_provincia : Optional[str]
    usu_canton    : Optional[str]
    usu_parroquia : Optional[str]
    usu_street1   : Optional[str]
    usu_street2   : Optional[str]
    usu_phone     : Optional[str]
    usu_phonehome : Optional[str]
    usu_numhome   : Optional[str]
    usu_email     : Optional[str]
    usu_password  : Optional[str]

class Usuario(UsuarioBase):
    
    class Config:
        orm_mode = True
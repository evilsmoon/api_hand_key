from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=BaseModel)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType]):
    def __init__(self,model:Type[ModelType]):
        self.model = model


    def get_all(
        self,db:Session
    )-> List[ModelType]:
    
        return db.query(self.model).offset(0).limit(10).all()

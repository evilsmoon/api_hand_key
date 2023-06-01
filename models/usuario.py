from sqlalchemy import Column,Text,Integer
from db.base_class import Base
class Usuario(Base):

    usu_id         = Column(Integer,primary_key=True)
    usu_name       = Column(Text)
    usu_lastname   = Column(Text)
    usu_country    = Column(Text)
    usu_province   = Column(Text)
    usu_canton     = Column(Text)
    usu_parish     = Column(Text)
    usu_street1    = Column(Text)
    usu_street2    = Column(Text)
    usu_phone      = Column(Text)
    usu_phonehome  = Column(Text)
    usu_numhome    = Column(Text)
    usu_email      = Column(Text)
    usu_password   = Column(Text)
 

  
  
  
  
  
  
  
  
  
  
  
  
  
 
 
   
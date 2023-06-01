from fastapi import APIRouter
from api.routers import login
                        # ,\
                        # predio,\
                        # usuario,\
                        # infraestructura,\
                        # edificacion
api_router = APIRouter()

api_router.include_router(login.router,
                            prefix="/login",
                            tags=['Login'])





from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List

from api.ip import ip_router
from validators.requests_ import IpsDataRequest

# from sftp_client import connect_sftp  # Импортируйте свою функцию для подключения к SFTP
# from main_script import process_files  # Импортируйте ваш код

app = FastAPI(
    title="IP-FINDER",
    description="IP-finder as RESTful API",
    version="3.0",
    docs_url="/",
    redoc_url=None,
    openapi_url="/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": True})


origins = ["http://localhost", "http://localhost:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(ip_router, prefix="/api/v1", tags=["IP-FINDER"])


# @app.post("/process-files")
# def process_files_endpoint(request: IpsDataRequest):
#     """
#     Endpoint для обработки файлов.
#     """
#     try:
#         # sftp = connect_sftp()  # Функция для подключения к SFTP
#         # process_files(sftp, request.files)  # Используйте вашу функцию для обработки файлов
#         # sftp.close()
#         return {"status": "success", "message": "Files processed successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

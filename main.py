import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.ip import ip_router

# from sftp_client import connect_sftp
# from main_script import process_files

app = FastAPI(
    title="IP-FINDER",
    description="IP-finder as RESTful API",
    version="3.0",
    docs_url="/",
    redoc_url=None,
    openapi_url="/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": True})


origins = ["http://localhost", "http://localhost:8000", "http://0.0.0.0:8248"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Define the environment variable DJANGO_SETTINGS_MODULE
# for DATABASES settings configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')

app.include_router(ip_router, prefix="/api/v1", tags=["IP-FINDER"])

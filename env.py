from dotenv import dotenv_values
from os import environ as env

environment: None | dict = None

if( not "ENV_PRODUCTION" in env ):
    environment = dotenv_values( "./.env" )
else:
    environment = env
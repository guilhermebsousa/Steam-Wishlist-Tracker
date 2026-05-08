import os
import time
import logging
from dotenv import load_dotenv
from src.extraction import extract_apps_info
from src.transformation import transformations
from src.load import app_verification, session
from src.notify import promo_alert
from src.tools import read_json, load_settings_yaml, logging_setup

logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()

env_path = config['paths']['env']
load_dotenv(env_path)

api_key = os.getenv('API_KEY')
steam_user_id = os.getenv('STEAM_USER_ID')
discord_webhook =  os.getenv('WEBHOOK')
apps_info = config['paths']['apps_info']



def pipeline():
    logger.info("Iniciando Pipeline...")
    logger.info("=========EXTRACT=========")
    extract_apps_info(steam_user_id, api_key)

    logger.info("=========TRANSFORM=========")
    transformations(apps_info)
    
    logger.info("=========LOAD=========")
    apps_data = read_json(apps_info)
    app_verification(session, apps_data)
    
    logger.info("=========NOTIFICATION=========")
    promo_alert(discord_webhook)
    logger.info("Pipeline Concluído!")

pipeline()


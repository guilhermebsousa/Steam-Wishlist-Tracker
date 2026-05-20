import requests
import logging
import json
from src.tools import save_json, logging_setup, load_settings_yaml

logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()


def get_wishlist(steam_id:str, api_key:str) -> list:
    logger.info("Iniciando extração da Wishlist...")

    try:
        url = config.get("urls", {}).get("get_wishlist").format(api_key=api_key, steam_id=steam_id)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return []
    
    app_ids = []
    items = data.get("response", {}).get("items")

    for app in items:
        app_ids.append(str(app["appid"]))
    
    save_json("./data/wishlist_ids.json", app_ids)
   
    logger.info(f" {len(app_ids)} ID's extraídos da Wishlist!")
    return app_ids


def extract_apps_info(steam_id:str, api_key:str) -> list[dict]:
    app_ids = get_wishlist(steam_id, api_key)

    apps_data = {}

    logger.info("Extraindo dados dos apps...")

    try:
        for app_id in app_ids:
            url = config.get("urls", {}).get("get_app_info").format(app_id=app_id)
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            apps_data[app_id] = data

        with open("./data/apps_info.json", 'w') as f:
            json.dump(apps_data, f, indent=4)
        
        logger.info("Dados dos apps extraídos!")
        return apps_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return {}


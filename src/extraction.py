import requests
import logging
import json
from src.tools import logging_setup, load_settings_yaml

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
    
    with open("./data/wishlist_ids.json", 'w') as f:
        json.dump(app_ids, f, indent=4)
    
    logger.info(f" {len(app_ids)} ID's extraídos da Wishlist!")
    return app_ids


def filter_game_data(app_id: str, data: dict) -> dict:
    game = data.get(app_id, {}).get("data")
    price = game.get("price_overview", {})
    genres = game.get("genres", [])

    return {
        "id": app_id,
        "name": game.get("name"),
        "initial_price": price.get("initial", 0),
        "final_price": price.get("final", 0),
        "discount_percent": price.get("discount_percent", 0),
        "main_genre": genres[0]["description"] if genres else "Sem gênero",
        "header_image": game.get("header_image", ""),
    }



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

            filtered = filter_game_data(app_id, data)

            apps_data[app_id] = filtered

        with open("./data/apps_info.json", 'w') as f:
            json.dump(apps_data, f, indent=4)
        
        logger.info("Dados dos apps extraídos!")
        return apps_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return {}

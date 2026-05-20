import logging
from src.tools import logging_setup, load_settings_yaml, read_json, save_json

logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()


def filter_game_data(file_path: str) -> None:
    formated_data = {}
    raw_data = read_json(file_path)
    for app_id, app_data in raw_data.items():
        game = app_data.get(app_id, {}).get("data")
        price = game.get("price_overview", {})
        genres = game.get("genres", [])

        formated_data[app_id] = {
            "id": app_id,
            "name": game.get("name"),
            "initial_price": price.get("initial", 0),
            "final_price": price.get("final", 0),
            "discount_percent": price.get("discount_percent", 0),
            "main_genre": genres[0]["description"] if genres else "Sem gênero",
            "header_image": game.get("header_image", "")
        }
    save_json("./data/apps_info.json", formated_data)


def price_formatation(apps_info: dict) -> None:
    logger.info("Ajustando formato de preços...")
    for app_id, app_data in apps_info.items():
        if app_data.get("initial_price") is not None:
            app_data["initial_price"] /= 100
        if app_data.get("final_price") is not None:
            app_data["final_price"] /= 100
    logger.info("Formato de preços ajustados com sucesso!")       
    return apps_info


def id_to_int(apps_info: dict) -> None:
    logger.info("Convertendo ID para formato inteiro...")
    for app_id, app_data in apps_info.items():
        app_data["id"] = int(app_data["id"])
    logger.info("Conversão realizada com sucesso!")
    return apps_info 


def transformations(file_path: str) -> None:
    logger.info("Iniciando transformações do arquivo...")
    filter_game_data(file_path)
    data = read_json(file_path)
    data = price_formatation(data)
    data = id_to_int(data)
    save_json("./data/apps_info.json", data)
    logger.info("Tranformações concluídas!")

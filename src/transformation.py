import logging
import pandas as pd
from src.tools import logging_setup, load_settings_yaml, read_json, save_json

logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()


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
    data = read_json(file_path)
    data = price_formatation(data)
    data = id_to_int(data)
    df = pd.DataFrame(data)
    save_json("./data/apps_info.json", data)
    logger.info("Tranformações concluídas!")
    return df

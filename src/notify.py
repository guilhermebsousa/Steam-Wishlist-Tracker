import requests
import logging
import json
from src.tools import read_json, load_settings_yaml, logging_setup, save_json


logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()


def notify(url: str, app: dict) -> None:
    template = read_json("./data/notification_template.json")
    
    template_str = json.dumps(template)
    
    template_str = template_str.replace("game_title", app.get("name", "Sem título"))
    template_str = template_str.replace("initial_price", str(app.get("initial_price", "0")))
    template_str = template_str.replace("final_price", str(app.get("final_price", "0")))
    template_str = template_str.replace("discount_percent", str(app.get("discount_percent", "0")))
    template_str = template_str.replace("header_image", app.get("header_image", ""))
    template_str = template_str.replace("main_genre", app.get("main_genre", "N/A"))
    template_str = template_str.replace("app_id", str(app.get("id", "N/A")))
    
    filled_template = json.loads(template_str)
    response = requests.post(url, json=filled_template)
    
    if response.status_code == 204:
        logger.info(f" Notificação de {app.get('name', 'Unknown')} enviada.")
    else:
        logger.error(f"Falha ao enviar: {response.status_code} - {response.text}")

def promo_alert(webhook_url: str) -> None:
    promo_ids_list = read_json('./data/promo_ids.json')
    notified = read_json('./data/notified.json')
    apps_info = read_json('./data/apps_info.json')
    
    logger.info(f"Verificado {len(promo_ids_list)} app(s) em promoção!")
    
    new_notifications = 0
    
    for app_id in promo_ids_list:
        if app_id not in notified:
            app_data = apps_info.get(app_id)
            if app_data:
                notify(webhook_url, app_data)
                notified.append(app_id)
                new_notifications += 1
            else:
                logger.warning(f"App {app_id} não encontrado no apps_info.json")
    
    if new_notifications == 0:
        logger.info("Nenhum novo app em promoção para notificar")
    
    logger.info(f"Verificando apps fora de promoção...")
    
    removed = 0
    for app_id in notified[:]:
        if app_id not in promo_ids_list:
            notified.remove(app_id)
            removed += 1
            logger.info(f"Removendo app fora de promoção: {app_id}")
    
    if removed > 0:
        logger.info(f"{removed} app(s) removido(s) da lista de notificados")
    
    save_json('./data/notified.json', notified)
    
    logger.info(f" Processo concluído! {new_notifications} notificação(ões) enviada(s)")

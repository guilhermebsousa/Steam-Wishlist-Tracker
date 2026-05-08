import json
import yaml
import logging

def logging_setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(filename)s | %(levelname)s | %(message)s"
    )

def load_settings_yaml():
    with open('./config/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)
        return settings
    

def read_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
    
def save_json(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)
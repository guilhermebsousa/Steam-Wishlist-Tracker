import os
import logging
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import quote_plus
from sqlalchemy import create_engine, String, Integer, Numeric, func, DateTime, Boolean
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from src.tools import load_settings_yaml, logging_setup, read_json, save_json


logger = logging.getLogger(__name__)
logging_setup()
config = load_settings_yaml()

env_path = config.get("paths", {}).get("env")
load_dotenv(env_path)

user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
host = 'localhost'

engine = create_engine(
    f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
)

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class App(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    initial_price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    final_price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    discount_percent: Mapped[int] = mapped_column(Integer)
    main_genre: Mapped[str] = mapped_column(String(30))
    header_image: Mapped[str] = mapped_column(String(500))
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now(),
                                                 onupdate=func.now()
                                                 )

Base.metadata.create_all(engine)


def update_app(session, app_data: dict) -> None:
    app = session.query(App).filter_by(id=app_data.get('id')).first()

    if app:
        app.name = app_data["name"]
        app.initial_price = app_data["initial_price"]
        app.final_price = app_data["final_price"]
        app.discount_percent = app_data["discount_percent"]
        app.main_genre = app_data["main_genre"]
        app.header_image = app_data["header_image"]

    else:
        app = App(**app_data)
        session.add(app)
        logger.info(f"NOVO APP: ID {app.id} adicionado")


def app_verification(session, json_data: dict[dict]) -> list:
    json_ids = list(json_data.keys())
    
    promo_ids = []
    
    logger.info("Iniciando verificação de Apps...")
    logger.info(f"Total de jogos no JSON: {len(json_data)}")
    
    logger.info("Atualizando colunas dos Apps e verificando promoções...")
    for app_id, app_data in json_data.items():
        update_app(session, app_data)

        if app_data.get("discount_percent", 0) > 0:
            promo_ids.append(str(app_id))
    logger.info("Atualização concluída!")
    
    logger.info("Verificando Apps para deletar...")

    to_delete = session.query(App).filter(
        App.id.notin_(json_ids)
    ).all()
    
    for app in to_delete:
        session.delete(app)
        logger.info(f"Jogo de ID {app.id} não encontrado no JSON, deletando...")
    
    if not to_delete:
        logger.info("Nenhum jogo precisou ser deletado.")

    logger.info("Verificação concluída!")
    session.commit()

    logger.info(f"Verificado(s) {len(promo_ids)} app(s) em promoção")
    save_json('./data/promo_ids.json', promo_ids)
    return promo_ids
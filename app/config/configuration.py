import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import StringConstraints
import pytz

load_dotenv()


class Config:
    # air alarms api
    # WEBHOOK_URL = "https://api.ukrainealarm.com/api/v3/webhook"
    ALARMS_API_KEY = os.environ.get("ALARMS_API_KEY")
    PREDICTION_KEY = os.environ.get("PREDICTION_KEY")
    LIST_OF_REGIONS_URL = "https://api.ukrainealarm.com/api/v3/regions"
    AIR_URL = "https://api.ukrainealarm.com/api/v3/alerts"
    EXCLUDED_REGIONS = {
        "Тестовий регіон", "Луганська область", "Автономна Республіка Крим"
    }
    # weather api
    WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

    STORAGE_PATH = os.path.join(Path(__file__).resolve().parents[2], "storage")

    VECTORIZERS_PATH = os.path.join(STORAGE_PATH, "vectorizers")
    TELEGRAM_VECTORIZER_PATH = os.path.join(VECTORIZERS_PATH, "telegram_tfidf_vectorizer.pkl")
    ISW_VECTORIZER_PATH = os.path.join(VECTORIZERS_PATH, "isw_tfidf_vectorizer.pkl")

    HOURLY_PREDICTIONS_PATH = os.path.join(STORAGE_PATH, "hourly_predictions")
    DATASETS_PATH = os.path.join(STORAGE_PATH, "datasets")

    PCAS_PATH = os.path.join(STORAGE_PATH, "pcas")
    TELEGRAM_PCA_PATH = os.path.join(PCAS_PATH, "telegram_pca_100.pkl")
    ISW_PCA_PATH = os.path.join(PCAS_PATH, "isw_pca_100.pkl")

    DOWNLOAD_DIRECTORY_NLTK = os.path.join(Path(__file__).resolve().parents[2], ".venv", "nltk_data")
    DOWNLOAD_DIRECTORY_STANZA = os.path.join(Path(__file__).resolve().parents[2], ".venv", "stanza_data")

    # ISW parser
    ISW_URL = "https://isw.pub/"

    ISW_PARQUET_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "isw_data.parquet"
    )
    ISW_CSV_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "isw_data.csv"
    )
    ISW_PICKLE_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "isw_data.pickle"
    )
    SHORT_REPORTS_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "short_reports"
    )
    FULL_REPORTS_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "full_reports"
    )
    LINKS_PATH = os.path.join(
        STORAGE_PATH, "isw_reports", "links"
    )

    URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]

    # telegram parser
    TELEGRAM_MESSAGES_PATH = os.path.join(STORAGE_PATH, 'telegram_messages')
    TELEGRAM_API_ID: int = os.environ.get('TELEGRAM_API_ID')
    TELEGRAM_API_HASH: str = os.environ.get('TELEGRAM_API_HASH')
    TELEGRAM_API_PHONE: str = os.environ.get('TELEGRAM_API_PHONE')

    LOCATION_DIST_DICT = {
        'Uzhgorod': 0.0,
        'Mykolaiv': 0.9235491341607043,
        'Lviv': 0.28420891204166954,
        'Lutsk': 0.4422902052447917,
        'Chernihiv': 0.9206616553025182,
        'Chernivtsi': 0.4753020511871291,
        'Vinnytsia': 0.6919239097568077,
        'Kharkiv': 0.9795021082216824,
        'Ternopil': 0.4585390194914293,
        'Kyiv': 0.856578878692158,
        'Kyiv oblast': 0.9260377782417122,
        'Rivne': 0.560432106947143,
        'Cherkasy': 0.8571012064607353,
        'Odesa': 0.8236921274833727,
        'Zaporozhye': 0.973444258724334,
        'Zhytomyr': 0.72135305632032,
        'Kherson': 0.9806117802336661,
        'Khmelnytskyi': 0.5876207028911374,
        'Ivano-Frankivsk': 0.2998301253195772,
        'Dnipro': 0.9513874520851243,
        'Kropyvnytskyi': 0.8833900343036755,
        'Poltava': 0.9587059984686096,
        'Sumy': 0.9819281785258528,
        'Donetsk': 0.9792767081873717
    }

    MODELS_PATH = os.path.join(STORAGE_PATH, 'models')
    MODEL_FOR_PREDICT_PATH = os.path.join(MODELS_PATH, '1_hist_gradient_boosting_classifier_v4.pkl')
    
    KYIV_TZ = pytz.timezone("Europe/Kyiv")


def init_dirs():
    dirs = [
        Config.STORAGE_PATH,
        Config.VECTORIZERS_PATH,
        Config.HOURLY_PREDICTIONS_PATH,
        Config.DATASETS_PATH,
        Config.PCAS_PATH,
        Config.DOWNLOAD_DIRECTORY_NLTK,
        Config.DOWNLOAD_DIRECTORY_STANZA,
        Config.SHORT_REPORTS_PATH,
        Config.FULL_REPORTS_PATH,
        Config.LINKS_PATH,
        Config.TELEGRAM_MESSAGES_PATH,
        Config.MODELS_PATH
    ]

    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

init_dirs()

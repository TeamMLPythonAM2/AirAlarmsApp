import asyncio
import os
import pandas as pd
import datetime as dt
import pytz

from app.config.configuration import Config
from app.core.scrapers.telegram.telegram_hourly_scraper import update_messages
from app.core.services.WeatherService import WeatherService
from app.core.services.AirAlarmsService import AirAlarmsService
from app.core.entities.WeatherDTO import WeatherDTO
from app.core.utils import telegram
from app.core.utils import isw
from app.core.utils.html_processing import load_latest_html_file
from app.core.utils.data_processing import *
from app.core.utils.predict import make_predictions, save_predictions


async def weather_dataframe() -> pd.DataFrame:
    weather_service = WeatherService()
    weathers: list[WeatherDTO] = []

    for location in Config.LOCATION_DIST_DICT.keys():
        weathers += await weather_service.request(location, now=True)

    df = pd.DataFrame([w.model_dump() for w in weathers])
    df['dist_from_front'] = df['city_address'].map(Config.LOCATION_DIST_DICT)
    df['day_hour'] = df['datetime'].dt.hour
    return df


async def telegram_dataframe() -> pd.DataFrame:
    date = await update_messages()

    path = os.path.join(Config.TELEGRAM_MESSAGES_PATH, f'{date.strftime('%Y-%m-%d_%H')}.csv')
    df = telegram.read_telegram_messages_csv(path)
    df = telegram.lemmatize_dataframe(df)
    df = df.groupby(['date'])['l_content'].agg(' '.join).reset_index()

    tfidf_matrix_pca = telegram.vectorize_dataframe(df)
    df['telegram_vector'] = tfidf_matrix_pca.tolist()

    return df.drop(columns=['l_content'])


async def isw_dataframe() -> pd.DataFrame:
    df = load_latest_html_file('2025')
    tfidf_matrix_pca = isw.vectorize_dataframe(df)
    df['isw_vector'] = tfidf_matrix_pca.tolist()

    return df.drop(columns=[
        'short_url',
        'full_url',
        'text_data',
        'html_data',
        'text_lemm',
        'text_stemm'
    ])


async def get_alarms_count():
    alert_info = await AirAlarmsService.request_current(all_oblasts=True)
    return len([x for x in alert_info if x.get("alert") == "AIR"])


async def predict():
    weather_df: pd.DataFrame = await weather_dataframe()
    telegram_df: pd.DataFrame = await telegram_dataframe()
    isw_df: pd.DataFrame = await isw_dataframe()
    alarms_count: int = await get_alarms_count()

    data = prepare_merged_dataframe(weather_df, telegram_df, isw_df, alarms_count)
    data = expand_vectors(data)

    dataset = data.drop(columns=['datetime', 'city_address'])
    predictions = make_predictions(dataset)

    kyiv_tz = pytz.timezone("Europe/Kyiv")
    date = dt.datetime.now(tz=kyiv_tz).replace(minute=0, second=0, microsecond=0)

    save_data(data, date)
    save_predictions(data, predictions, date)


if __name__ == '__main__':
    asyncio.run(predict())

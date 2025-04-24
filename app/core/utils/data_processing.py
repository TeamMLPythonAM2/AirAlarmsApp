import pandas as pd
import datetime as dt
import os

from app.config.configuration import Config


def prepare_merged_dataframe(
        weather_df: pd.DataFrame,
        telegram_df: pd.DataFrame,
        isw_df: pd.DataFrame,
        alarms_count: int
) -> pd.DataFrame:
    telegram_vectors = pd.concat([telegram_df[["telegram_vector"]]] * len(weather_df), ignore_index=True)
    isw_vectors = pd.concat([isw_df[["isw_vector"]]] * len(weather_df), ignore_index=True)

    merged_df = pd.concat([
        weather_df.reset_index(drop=True),
        telegram_vectors.reset_index(drop=True),
        isw_vectors.reset_index(drop=True),
        pd.Series(alarms_count, index=range(len(weather_df)), name='alarms_hourly')
    ], axis=1)

    return merged_df


def expand_vectors(df: pd.DataFrame) -> pd.DataFrame:
    vector_isw = df['isw_vector'].apply(pd.Series)
    vector_isw.columns = [f'isw_{i}' for i in range(vector_isw.shape[1])]
    df = pd.concat([df.drop(columns=['isw_vector']), vector_isw], axis=1)

    vector_tg = df['telegram_vector'].apply(pd.Series)
    vector_tg.columns = [f'telegram_{i}' for i in range(vector_tg.shape[1])]
    df = pd.concat([df.drop(columns=['telegram_vector']), vector_tg], axis=1)

    return df


def save_data(data: pd.DataFrame, date: dt.datetime) -> None:
    df = data.drop_duplicates(subset="city_address").copy()
    df['datetime'] = date
    df['day_hour'] = date.hour

    path = os.path.join(Config.DATASETS_PATH, f'{date.strftime('%Y-%m-%d_%H')}.parquet')
    df.to_parquet(path, index=False)

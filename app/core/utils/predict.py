import pandas as pd
import numpy as np
import joblib
import datetime as dt
import os

from app.config.configuration import Config


def make_predictions(df: pd.DataFrame):
    model = joblib.load(Config.MODEL_FOR_PREDICT_PATH)
    df = df[model.feature_names_in_]
    return model.predict(df)


def save_predictions(df: pd.DataFrame, predictions: np.array, date: dt.datetime):
    data = pd.concat([
        df[['datetime', 'city_address']].reset_index(drop=True),
        pd.Series(predictions, name='predict')
    ], axis=1)

    path = os.path.join(Config.HOURLY_PREDICTIONS_PATH, f'{date.strftime('%Y-%m-%d_%H')}.parquet')
    data.to_parquet(path, index=False)

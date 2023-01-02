import os
import time
from datetime import datetime, timedelta

import joblib
import pandas as pd
import requests
from sqlalchemy import Column, Float, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base
from utils import get_historical_temperature, pickle_path

lat = 52.084516
lon = 5.115539
api_key = os.environ.get("API_KEY")

Base = declarative_base()


class Temperatures(Base):
    __tablename__ = "temperatures"
    timestamp = Column(Integer, primary_key=True)
    forecast_temperature = Column(Float)
    actual_temperature = Column(Float)


def predict_latest():
    """
    In order to create the model input features, 24 hours of historical temperatures are needed.
    For that reason this method takes 2 days of API history and filters to the last 24 records.
    This script only prints the prediction (an array of length 1) and does not implement any storage.
    """

    prediction_range = pd.date_range(end=pd.Timestamp.now().date(), periods=2, freq="d")
    df_pred = get_historical_temperature(prediction_range).iloc[-25:]
    pipeline = joblib.load(pickle_path)

    return pipeline.predict(df_pred)


def insert_forecast_value(session, timestamp):
    forecast = predict_latest()[0]

    instance = (
        session.query(Temperatures)
        .filter_by(
            timestamp=timestamp, forecast_temperature=forecast, actual_temperature=None
        )
        .one_or_none()
    )
    if not instance:
        temperature = Temperatures(
            timestamp=timestamp, forecast_temperature=forecast, actual_temperature=None
        )
        session.add(temperature)
    else:
        session.query(Temperatures).filter_by(timestamp=timestamp).update(
            {"forecast_temperature": forecast}
        )
    session.commit()


def get_current_temperature(timestamp):
    api_call = (
        f"https://api.openweathermap.org/data/2.5/onecall/timemachine"
        f"?lat={lat}&lon={lon}&dt={timestamp}&units=metric"
        f"&appid={api_key}&only_current={{true}}"
    )
    result = requests.get(api_call).json()["current"]["temp"]
    return result


def update_actual_value(session, timestamp):
    current_temperature = get_current_temperature(timestamp)

    instance = (
        session.query(Temperatures)
        .filter_by(
            timestamp=timestamp,
        )
        .one_or_none()
    )
    if not instance:
        temperature = Temperatures(
            timestamp=timestamp,
            forecast_temperature=None,
            actual_temperature=current_temperature,
        )
        session.add(temperature)
    else:
        session.query(Temperatures).filter_by(timestamp=timestamp).update(
            {"actual_temperature": current_temperature}
        )
    session.commit()


def save_to_db():
    con = "postgresql+psycopg2://root:root@pgdatabase:5432/weather_data"
    engine = create_engine(con)
    with Session(engine) as session:
        Base.metadata.create_all(engine)

        execution_date = datetime.fromisoformat(os.environ.get("DT")).replace(
            microsecond=0, second=0, minute=0
        )

        forecast_timestamp = int(
            time.mktime((execution_date + timedelta(hours=1)).timetuple())
        )
        update_timestamp = int(time.mktime(execution_date.timetuple()))

        insert_forecast_value(session, forecast_timestamp)
        update_actual_value(session, update_timestamp)


if __name__ == "__main__":
    save_to_db()

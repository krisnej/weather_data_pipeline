FROM python:3.8

RUN pip install scikit-learn==0.24.2 pandas==1.5.1 requests==2.24.0 psycopg2==2.9.5 sqlalchemy==1.4.44

COPY ./dags/temperature_forecast ./temperature_forecast

ENV API_KEY [valid_api_key]

ENTRYPOINT python temperature_forecast/predict.py
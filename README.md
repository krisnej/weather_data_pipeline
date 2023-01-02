# Context

This is a batch data pipeline that processes data from a weather API on a structural basis. 
The API used is OpenWeatherMap (https://openweathermap.org/api/one-call-api). 
An API key can be generated via their website, it is free tiered and rate-limited at **60 calls per minute**.

# Deploying a temperature forecast
The aim is to create an hourly batch job that predicts the temperature for the next hour. 
An ML model can be trained on hourly historical data. 
The API's free tier returns max 5 days of history, hence this is the extent of the training set that was used.

Description of the data science code:

    ├── temperature_forecast
    │   ├── train.py        <- Script that can be used to retrain the model on the last ~5 days of API data
    │   ├── predict.py      <- Script that makes a prediction using the latest 24 hours of API data
    │   ├── utils.py        <- Helper functions & API parameters
    │   └── pipeline.pkl    <- Stored model pickle to be used for predictions

# Implementation
The solution :
* Uses a proper scheduling tool for running your batch job
* Uses Docker for running services locally and/or for containerizing job code:
  * docker-compose to set up the necessary services (which communicate with each other). 
  * The DAG tasks themselves also run as Docker containers.
* Runs the logic from `predict.py` and stores the result in a database (a single prediction each time)
* Stores the real temperature values (which will be available an hour later)
* Runs a separate training pipeline that retrains the model daily

# Architecture

![Architecture Diagram](diagram.jpg)

# How to run

Run `make airflow` to build the airflow containers, the Postgres database for the weather data
and the Docker image used in the DAG. Trigger the DAG manually in the UI or add a schedule in `predict_dag.py`. 

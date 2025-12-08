from fastapi import FastAPI
import database as db

app = FastAPI()

@app.get("/")
def home():
    return {'message': 'Finance Data API, visit /docs.'}

@app.get("/countries")
def countries():
    data = db.select('country_name', 'countries')

    countries = []
    for item in data:
        countries.append(item[0])

    return countries

@app.get("/metrics")
def metrics():
    data = db.select('metric_name', 'metrics')

    metrics = []
    for item in data:
        metrics.append(item[0])

    return metrics

@app.get("/data/{country}/{metric}")
def get_country_metric_data(country: str, metric: str):
    country_id = db.get_country_id(country)
    metric_id = db.get_metric_id(metric)

    data = db.get_data_country_metric(
        country_id=country_id, 
        metric_id=metric_id)
    
    return data

@app.get("/data/{country}/{metric}/latest")
def get_country_metric_data_latest(country: str, metric: str):
    country_id = db.get_country_id(country)
    metric_id = db.get_metric_id(metric)

    data = db.get_data_country_metric_latest(
        country_id=country_id, 
        metric_id=metric_id)
    
    return data

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

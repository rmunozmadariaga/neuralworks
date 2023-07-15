from fastapi import FastAPI
from app.services import data_manipulation


app = FastAPI(
    # openapi_tags=tags_metadata,
    title="NeuralWorks DE Test",
    description="Repositorio y documentacion: [GitHub](https://github.com/rmunozmadariaga/neuralworks)",
    version="0.0.1",
    docs_url="/",
    redoc_url="/docs",
    )


@app.get("/")
def read_root():
    return {"API OK"}


@app.get("/extract_trips")
def extract_data():
    data = data_manipulation.extract_transform_load()
    return data


@app.get("/similar_trips")
def similar(from_date: str, to_date: str, margin: str, lon_o: str, lat_o: str, lon_d: str, lat_d: str):
    similar_data = data_manipulation.similar_trips(from_date, to_date, margin, lon_o, lat_o, lon_d, lat_d)
    return similar_data


@app.get("/boundbox_trips")
def box(from_date: str, to_date: str, region: str, lon_min: str, lat_min: str, lon_max: str, lat_max: str):
    box_trips_data = data_manipulation.box_trips(from_date, to_date, region, lon_min, lat_min, lon_max, lat_max)
    return box_trips_data

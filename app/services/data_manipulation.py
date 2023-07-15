import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely import wkt
from datetime import datetime

DB_URL = os.getenv('DB_URL')


def extract_transform_load():

    engine = create_engine(DB_URL)

    # EXTRACT
    df_csv = pd.read_csv('trips.csv')
    df_csv_aux = df_csv

    # TRANSFORM
    df_csv['geometry'] = df_csv['origin_coord']
    df_csv['geometry'] = df_csv['geometry'].apply(wkt.loads)

    # ORIGIN (LAT, LON)
    gdf_origin = gpd.GeoDataFrame(df_csv, crs='epsg:4326')
    gdf_origin['lon_o'] = gdf_origin.geometry.x
    gdf_origin['lat_o'] = gdf_origin.geometry.y

    # DESTINATION (LAT, LON)
    df_csv_aux['geometry'] = df_csv_aux['destination_coord']
    df_csv_aux['geometry'] = df_csv_aux['geometry'].apply(wkt.loads)
    gdf_destination = gpd.GeoDataFrame(df_csv_aux, crs='epsg:4326')
    gdf_destination['lon_d'] = gdf_destination.geometry.x
    gdf_destination['lat_d'] = gdf_destination.geometry.y

    # PRE LOAD (CLEANING DF)
    full_df = gdf_origin.merge(gdf_destination, how='left',
                               on=['datetime', 'region', 'origin_coord', 'destination_coord', 'datasource'])

    df = full_df.drop(['geometry_x', 'geometry_y'], axis=1)

    # LOAD
    df.to_sql('trips', con=engine, if_exists='replace')

    return str(len(df)) + ' registros cargados'


def similar_trips(from_date, to_date, margin, lon_o, lat_o, lon_d, lat_d):

    engine = create_engine(DB_URL)

    sql = "SELECT region, origin_coord, destination_coord, datetime, datasource FROM trips " \
          "WHERE lon_o BETWEEN " + lon_o + " - " + margin + " AND " + lon_o + " + " + margin + " " \
          "AND lat_o BETWEEN " + lat_o + " - " + margin + " AND " + lat_o + " + " + margin + " " \
          "AND lon_d BETWEEN " + lon_d + " - " + margin + " AND " + lon_d + " + " + margin + " " \
          "AND lat_d BETWEEN " + lat_d + " - " + margin + " AND " + lat_d + " + " + margin + " " \
          "AND datetime BETWEEN '" + from_date + "' AND '" + to_date + "'"
    df_proj = pd.read_sql_query(sql, con=engine)

    return df_proj.to_dict(orient="records")


def box_trips(from_date, to_date, region, lon_min, lat_min, lon_max, lat_max):

    engine = create_engine(DB_URL)

    from_month = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S').month
    from_year = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S').year
    to_month = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S').month
    to_year = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S').year

    if from_month == to_month and from_year == to_year:
        sql = "SELECT count(1) FROM trips " \
              "WHERE region = '" + region + "' " \
              "AND lon_o BETWEEN " + lon_min + " AND " + lon_max + " " \
              "AND lat_o BETWEEN " + lat_min + " AND " + lat_max + " " \
              "AND lon_d BETWEEN " + lon_min + " AND " + lon_max + " " \
              "AND lat_d BETWEEN " + lat_min + " AND " + lat_max + " " \
              "AND datetime BETWEEN '" + from_date + "' AND '" + to_date + "'"
        week_trips = pd.read_sql_query(sql, con=engine)

        sql2 = "SELECT count(1) FROM trips " \
               "WHERE region = '" + region + "' " \
               "AND lon_o BETWEEN " + lon_min + " AND " + lon_max + " " \
               "AND lat_o BETWEEN " + lat_min + " AND " + lat_max + " " \
               "AND lon_d BETWEEN " + lon_min + " AND " + lon_max + " " \
               "AND lat_d BETWEEN " + lat_min + " AND " + lat_max + " " \
               "AND date_part('month', datetime::timestamp::date) = '" + str(to_month) + "' " \
               "AND date_part('year', datetime::timestamp::date) = '" + str(to_year) + "'"
        count_trips = pd.read_sql_query(sql2, con=engine)

        stats_trips = pd.merge(week_trips, count_trips, left_index=True, right_index=True)
        stats_trips['avg'] = stats_trips['count_x'] / stats_trips['count_y']
        df = stats_trips.rename(columns={'count_x': 'week_trips', 'count_y': 'month_trips'})
        print(df)

        return df.to_dict(orient="records")
    else:
        return from_date + ' y ' + to_date + ' no comparten mes o anio. Favor ingresar fechas validas'

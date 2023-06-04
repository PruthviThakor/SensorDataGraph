import sys
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point,WritePrecision,InfluxDBClient
import datetime
import random
import uuid
sys.path.insert(0, r'../backend/')
from db.dbclient import InfluxDatabase
from db.consts import *

def random_ppm():
    return random.uniform(0,1000)

def random_type():
    return random.choice(["multivariate", "univariate"])

def set_sensor_id():
    return uuid.uuid4().int

def insert_data(n):
    influxdb = InfluxDatabase(DB_TOKEN,DB_ORG,DB_BUCKET,DB_URL)
    dbclient = influxdb.connect()
    write_api = dbclient.write_api(write_options=SYNCHRONOUS)

    for i in range(n):
        sensor_id = set_sensor_id()
        data_type_of_sensor = random_type()
        field_value = random_ppm()
        time = (datetime.datetime.now() + datetime.timedelta(seconds=-5*i))
        p = Point("o2_reading").tag("sensor_name", "o2").tag("subsensor", "o2").tag("sensor_id", sensor_id).tag("data_type_of_sensor", data_type_of_sensor).field("value", field_value).field("units", "ppm").time(time,WritePrecision.NS)
        write_api.write(DB_BUCKET, DB_ORG, p)


def get_data():
    influxdb = InfluxDatabase(DB_TOKEN,DB_ORG,DB_BUCKET,DB_URL)
    dbclient = influxdb.connect()
    query = f'from(bucket: "{DB_BUCKET}") |> range(start: -1y,stop: 1y)'
    tables = dbclient.query_api().query(query, org=DB_ORG)
    results = []
    for table in tables: 
        result = dict()
        for record in table.records: 
            result["measurement"] = record.get_measurement()
            result[record.get_field()] = record.get_value() 
            result["time"] = record.get_time().strftime("%m/%d/%Y, %H:%M:%S")
            result["sensor_name"] = record.values.get('sensor_name')
            result["subsensor"] = record.values.get('subsensor')
            result["sensor_id"] = record.values.get('sensor_id')
            result["data_type_of_sensor"] = record.values.get('data_type_of_sensor')
        results.append(result)
    return results


def get_specific_sensor(id):
    influxdb = InfluxDatabase(DB_TOKEN,DB_ORG,DB_BUCKET,DB_URL)
    dbclient = influxdb.connect()
    query = f'from(bucket: "{DB_BUCKET}") |> range(start: -1y,stop: 1y) |> filter(fn:(r) => r.sensor_id == "{id}")'
    tables = dbclient.query_api().query(query, org=DB_ORG)
    results = []
    for table in tables: 
        result = dict()
        for record in table.records:
            result[record.get_field()] = record.get_value() 
            result["time"] = record.get_time().strftime("%m/%d/%Y, %H:%M:%S")
        results.append(result)
    return results

def get_flitered_data(field=None, start="-1y", stop="1y", data_type_of_sensor=None):
    query = f'from(bucket: "{DB_BUCKET}") |> range(start: {start},stop: {stop})'
    if field is not None and data_type_of_sensor is None:
        query = f'from(bucket: "{DB_BUCKET}") |> range(start: {start},stop: {stop}) |> filter(fn:(r) => r._field == "{field}")'
    elif data_type_of_sensor is not None and field is None:
        query = f'from(bucket: "{DB_BUCKET}") |> range(start: {start},stop: {stop}) |> filter(fn:(r) => r.data_type_of_sensor == "{data_type_of_sensor}") '
    elif data_type_of_sensor is not None and field is not None:
        query = f'from(bucket: "{DB_BUCKET}") |> range(start: {start},stop: {stop}) |> filter(fn:(r) => r._field == "{field}") |> filter(fn:(r) => r.data_type_of_sensor == "{data_type_of_sensor}") '
        
    influxdb = InfluxDatabase(DB_TOKEN,DB_ORG,DB_BUCKET,DB_URL)
    dbclient = influxdb.connect()
    tables = dbclient.query_api().query(query, org=DB_ORG)
    results = []
    for table in tables: 
        result = dict()
        for record in table.records: 
            result["measurement"] = record.get_measurement()
            result[record.get_field()] = record.get_value() 
            result["time"] = record.get_time().strftime("%m/%d/%Y, %H:%M:%S")
            result["sensor_name"] = record.values.get('sensor_name')
            result["subsensor"] = record.values.get('subsensor')
            result["sensor_id"] = record.values.get('sensor_id')
            result["data_type_of_sensor"] = record.values.get('data_type_of_sensor')
        results.append(result)
    return results

def add_data_point(data):
    influxdb = InfluxDatabase(DB_TOKEN,DB_ORG,DB_BUCKET,DB_URL)
    dbclient = influxdb.connect()
    write_api = dbclient.write_api(write_options=SYNCHRONOUS)
    sensor_id = set_sensor_id()
    data_type_of_sensor = data['data_type_of_sensor'] if data['data_type_of_sensor'] in ["multivariate", "univariate"] else None
    field_value = float(data['field_value'])
    field_units = data['field_units']
    time = (datetime.datetime.now())
    p = Point("o2_reading").tag("sensor_name", "o2").tag("subsensor", "o2").tag("sensor_id", sensor_id).tag("data_type_of_sensor", data_type_of_sensor).field("value", field_value).field("units", field_units).time(time,WritePrecision.NS)
    write_api.write(DB_BUCKET, DB_ORG, p)
    
    return sensor_id
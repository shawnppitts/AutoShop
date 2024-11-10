from dotenv import load_dotenv
import os
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', '.env'))
load_dotenv(env_path)

INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
INFLUX_ORG = os.getenv("INFLUX_ORG")

# Print environment variables for debugging
print(f"INFLUXDB_TOKEN: {INFLUXDB_TOKEN}")
print(f"INFLUX_URL: {INFLUX_URL}")
print(f"INFLUX_BUCKET: {INFLUX_BUCKET}")
print(f"INFLUX_ORG: {INFLUX_ORG}")

def write_point(metric_name,path,field,value):
    try:
        # Initialize the InfluxDBClient inside the function
        write_client = InfluxDBClient(url=INFLUX_URL, token=INFLUXDB_TOKEN, org=INFLUX_ORG)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)
        
        # Create the point
        point = (
            Point(f"{metric_name}")
            .tag("url", f"{path}")
            .field(f"{field}", value)
        )
        
        # Write to the database
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"Point written: {name}, {field}, {value}")
    
    except AttributeError as e:
        print(f"Error: {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
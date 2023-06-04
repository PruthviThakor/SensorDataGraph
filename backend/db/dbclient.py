"""
Client class for interacting with Database
"""

from influxdb_client import InfluxDBClient, Point


class InfluxDatabase():
    def __init__(self,token=None,org=None,bucket=None,url="http://localhost:8086"):
        self.token = token
        self.org = org
        self.bucket = bucket
        self.url = url
        
    def connect(self):
        return InfluxDBClient(url=self.url, token=self.token)
    
    
    
        
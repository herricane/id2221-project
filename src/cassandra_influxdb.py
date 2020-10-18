from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from influxdb import InfluxDBClient
import datetime
from time import sleep


def data_transfer():
    while(True):
        date_utc = datetime.datetime.utcnow()
        past_utc = date_utc - datetime.timedelta(seconds=2)
        time_now = date_utc.strftime('%X')
        time_past = past_utc.strftime('%X')

        query = "SELECT * FROM <table> WHERE time > " + time_past + " AND time <= " + time_now + ";"
        rows = session.execute(query)
        influxdb_append(rows)

        sleep(2)

def influxdb_append(rows):
    points = []
    for row in rows:
        point = {
            "measurement": "<measurement>",
            "fields": {
                "track": row.track,
                "artist": row.artist,
                "genre": row.genre
            }
        }
        points.append(point)
    client.write_points(database='<database>', points=points)


if __name__ == '__main__':
    client = InfluxDBClient()
    client.create_database('<database>')

    cluster = Cluster(['localhost'])
    session = cluster.connect('<FILL IN keyspace>')

    data_transfer()

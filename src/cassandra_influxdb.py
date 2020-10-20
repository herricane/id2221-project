from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement, dict_factory
from influxdb import InfluxDBClient
import datetime
from time import sleep


def data_transfer():
    while(True):
        date_utc = datetime.datetime.now() - datetime.timedelta(seconds=30)
        past_utc = date_utc - datetime.timedelta(seconds=5)
        time_now = str(date_utc.timestamp()).split('.')[0]
        time_past = str(past_utc.timestamp()).split('.')[0]

        print(time_now)

        query = "SELECT * FROM mytable2 WHERE time > '" + str(time_past) + "' AND time <= '" + str(time_now) + "' ALLOW FILTERING;"
        rows = session.execute(query)

        influxdb_append(rows)

        sleep(5)

def influxdb_append(rows):
    points = []
    for row in rows:
        print(row)
        point = {
            "measurement": "mymea2",
            "tags": {
                "track_name": row['track_name'],
                "artist": row['artist'],
                "genre": row['genres']
            },
            "fields": {
                "value": 1
            }
        }
        points.append(point)
    client.write_points(database='mydb1', points=points)


if __name__ == '__main__':
    client = InfluxDBClient()
    client.create_database('mydb1')

    cluster = Cluster(['localhost'])
    session = cluster.connect('mykeyspace1')
    session.row_factory = dict_factory

    data_transfer()

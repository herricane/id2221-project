import logging
from cassandra.cluster import Cluster
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark_cassandra
from pyspark_cassandra import streaming
import json
import os
from spotify_caller import *



def create_stream():
    appName = 'twitterStreaming'
    master = 'local[2]'
    conf = SparkConf().setAppName(appName).setMaster(master)
    sc = SparkContext(conf=conf)
    return sc

if __name__ == "__main__":

    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2,anguenot/pyspark-cassandra:2.4.0 pyspark-shell'

    # Connect to cassandra
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    KEYSPACE = "mykeyspace1"
    TABLE = "mytable1"

    
    if KEYSPACE not in cluster.metadata.keyspaces:
        q = "CREATE KEYSPACE " + KEYSPACE + " WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' };"
        session.execute(q)

    session.set_keyspace(KEYSPACE)
    q = "CREATE TABLE IF NOT EXISTS " + KEYSPACE + "." + TABLE +  " (time text, track_name text, artist text, genres text, PRIMARY KEY(track_name));"
    session.execute(q)

    


    # Create a StreamingContext with batch interval of 3 second
    sc = create_stream()
    ssc = StreamingContext(sc, 3)

    topic = ["twitter"]
    kafkaParams = {"metadata.broker.list": "localhost:9092","zookeeper.connect": "localhost:2181"}
    kafkaStream = KafkaUtils.createDirectStream(ssc, topics=topic, kafkaParams=kafkaParams)

    # Message Processing
    lines = kafkaStream.map(lambda v: json.loads(v[1]))   # {'time': time, 'track_id': track_id}

    spotify = SpotifyClient()                            #{'name': track_name, 'artist': artist_name, 'genres': genres}
    rows = lines.map(lambda v: {"time": v['time'],  
                                "track_name": spotify.get_info(track_id=v['track_id'])['name'],
                                "artist": spotify.get_info(track_id=v['track_id'])['artist'],
                                "genres": spotify.get_info(track_id=v['track_id'])['genres']})
    rows.pprint()


    # Save to Cassandra
    rows.saveToCassandra(KEYSPACE,TABLE)


    ssc.start()
    ssc.awaitTermination()




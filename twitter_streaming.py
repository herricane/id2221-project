import json
import sys
import tweepy
import pykafka
from credentials import *


class KafkaStreamListener(tweepy.StreamListener):
    def __init__(self, topic):
        self.client = pykafka.KafkaClient("localhost:9092")
        self.producer = self.client.topics[topic].get_producer()

    def on_data(self, data):
        data_json = json.loads(data)
        urls = data_json["entities"]["urls"]
        if (len(urls) > 0):
            data_url = urls[0]["expanded_url"]
            print(data_url)
            self.producer.produce(bytes(data_url, encoding="utf8"))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print(
                """
                You have exceeded the limited number of attempts. 
                Please wait or the waiting time will increase exponentially after a failed attempt.
                """
            )
            return False
        else:
            return True

def twitter_setup():
    """
    Setup credentials for Twitter API.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

if __name__ == "__main__":
    topic = sys.argv[1]

    api = twitter_setup()
    twitter_stream = tweepy.Stream(api.auth, KafkaStreamListener(topic))
    twitter_stream.filter(languages=["en"], track=["open spotify com"])

import tweepy
import pykafka
from credentials import *

def twitter_setup():
    '''
    Setup credentials for Twitter API.
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

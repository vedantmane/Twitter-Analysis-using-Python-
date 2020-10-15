from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import Cursor

import numpy as np
import pandas as pd

import twitter_credentials
print("Libraries Imported Successfully!")

# Hashtags = ['Data Science', 'Artificial Intelligence', 'Machine Learning', 'Deep Learning']

## Twitter AUTHENTICATION
class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)        
        return auth

## Twitter CLIENT
class TwitterClient():
    def __init__(self, twitter_user = None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client

    """        
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    """
    
    
    def getTweets(self, count, hashtags):
        tweets = []
        last_id = -1
        if len(tweets) < count:
            while len(tweets) <= count:
                count_tweets = count - len(tweets)
                try:
                    new_tweets = api.search(q = hashtags, lang = 'en', count = count_tweets,
                                            max_id = str(last_id - 1))
                    if not new_tweets:
                        break
                    tweets.extend(new_tweets)
                    last_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    break
        return tweets


"""
class TwitterStreamer():
    #Class for Streaming and Processing Live Tweets!
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
        
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #Handle Twitter Authentication and connection to the Twitter Streaming API

        listener = TwitterListener(fetched_tweets_filename)
        
        auth = self.twitter_authenticator.authenticate_twitter_app()
        
        stream = Stream(auth, listener)
        stream.filter(track = hash_tag_list)
"""

"""
class TwitterListener(StreamListener):
    #Listens to the Tweets from the Twitter Streamer API...
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                #print(data)
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    
    def on_error(self, status):
        if status == 420:
            #Returning False in case rate limit reached... 
            return False
        print(status)
"""

class DataFrameGenerator():
    """
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data = [[tweet.id, tweet.text, len(tweet.text), tweet.favorite_count, tweet.retweet_count, tweet.created_at, tweet.source] 
                                  for tweet in tweets], 
                          columns = ['Id', 'Tweets', 'Length', 'Likes', 'Retweets', 'Created_at', 'Source'])
        return df
    

if __name__ == "__main__":
    
    hashtags = ['travel', 'wanderlust']
    
    count = int(input("Enter Number of Tweets to Fetch:\n"))
    
    #print("\nPress Ctrl + c to interupt...\n")
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hashtags)   
    
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    
    tweets = twitter_client.getTweets(count, hashtags)
    
    #print(dir(tweets[0]))
    
    frame_generator = DataFrameGenerator()
    df = frame_generator.tweets_to_data_frame(tweets)
    
    print(df.head(10))

    df.to_csv("tweets_new.csv", index = False, header = True)
    
    print("Data saved to tweets.csv file")

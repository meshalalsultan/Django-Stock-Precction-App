
import datetime

import time
import pandas as pd
import numpy as np
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import re

  


# keys and tokens from the Twitter Dev Console 
consumer_key = 'pj6YNhZZBugJ2iVTzprRFeyVv'
consumer_secret = 'vV71WKQdcaMuhYIDKufIdSOAxwiydLGGskpj0bueAPeOKruwoT'
access_token = '1184086168608088064-863KtlQN4hww75kvv8J5OpAn0nNnzj'
access_token_secret = 'bdwBvlMmpLT2WYDBo9rQNMFtuldjduOoPXOHsi6rmehwT'
  
        # attempt authentication 

        # create OAuthHandler object 
auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
auth.set_access_token(access_token, access_token_secret) 
        # create tweepy API object to fetch tweets 
api = tweepy.API(auth) 

  
def cleanTxt(tweet): 
        ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
        '''
        tweets = re.sub('@[A-Za-z0–9]+', '', tweet) #Removing @mentions
        tweets = re.sub('#', '', tweet) # Removing '#' hash tag
        tweets = re.sub('RT[\s]+', '', tweet) # Removing RT
        tweets = re.sub('https?:\/\/\S+', '', tweet) # Removing hyperlink
        #tweets=  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
        return tweets


def getSubjectivity(tweet):
        return TextBlob(tweet).sentiment.subjectivity

def getPolarity(tweet):
        return TextBlob(tweet).sentiment.polarity

def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'

def get_tweet(query):
    
    msgs = []
    msg =[]
    for tweets in api.search(query, count = 500 ):
        msg = [tweets.text] 
        msg = tuple(msg)                    
        msgs.append(msg)

    df = pd.DataFrame(msgs)
    df['Tweets'] = df[0].apply(cleanTxt)
    df.drop(0, axis=1, inplace=True)
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    positive = df.loc[df['Analysis'].str.contains('Positive')]
    negative = df.loc[df['Analysis'].str.contains('Negative')]
    neutral = df.loc[df['Analysis'].str.contains('Neutral')]
    df.to_csv('tweet_df.csv')

    positive_per = round((positive.shape[0]/df.shape[0])*100, 1)
    negative_per = round((negative.shape[0]/df.shape[0])*100, 1)
    neutral_per = round((neutral.shape[0]/df.shape[0])*100, 1)

    return positive_per , negative_per , neutral_per 

'''               
def get_tweet_sentiment(tweet): 
    
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
 

def get_tweets(query, count = 100): 

        # empty list to store parsed tweets 
        tweets = [] 
   
        # call twitter api to fetch tweets 
        fetched_tweets = api.search(q = query, count = count) 
  
        # parsing tweets one by one 
        for tweet in fetched_tweets: 
            # empty dictionary to store required params of a tweet 
            parsed_tweet = {} 

  
            # saving text of tweet 
            parsed_tweet['text'] = tweet.text 
            # saving sentiment of tweet 
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text) 
  
            # appending parsed tweet to tweets list 
            if tweet.retweet_count > 0: 
                # if tweet has retweets, ensure that it is appended only once 
                if parsed_tweet not in tweets: 
                    tweets.append(parsed_tweet) 
            else: 
                tweets.append(parsed_tweet) 
  
        # return parsed tweets 
        return tweets 
  
  

    # picking negative tweets from tweets 
    # percentage of negative tweets 
    # percentage of neutral tweets 
    st.text("Neutral tweets percentage: {} % \ ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 
  
    # printing first 5 positive tweets 
    st.text("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        st.write(tweet['text']) 
  
    # printing first 5 negative tweets 
    st.text("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        st.write(tweet['text']) 
  
'''

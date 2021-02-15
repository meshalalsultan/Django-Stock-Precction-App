#  -*- coding: utf-8 -*-
import csv
import math
import re
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tweepy
from bs4 import BeautifulSoup
from keras.layers import Dense, Flatten, LSTM
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from nltk.corpus import stopwords   # Import the stop word list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from textblob import TextBlob

# Fix random seed for reproducibility
seed = 7
np.random.seed(seed)

CONSUMER_KEY = 'pj6YNhZZBugJ2iVTzprRFeyVv'
CONSUMER_SECRET = 'vV71WKQdcaMuhYIDKufIdSOAxwiydLGGskpj0bueAPeOKruwoT'
ACCESS_TOKEN = '1184086168608088064-863KtlQN4hww75kvv8J5OpAn0nNnzj'
ACCESS_TOKEN_SECRET = 'bdwBvlMmpLT2WYDBo9rQNMFtuldjduOoPXOHsi6rmehwT'

# API keys

# Price training and testing set
prices_train_test = []

# Tweet sentiment training and testing set
tweets_train_test = []


# Twitter authentication and search
def twitter_search(text, limit=20):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    
    api = tweepy.API(auth, wait_on_rate_limit_notify=True)
    tweets = []
    
    # Define a threshold for each sentiment to classify each
    # as positive(1) or negative(0).
    threshold = 0.1
    pos_tweets = 0
    neg_tweets = 0
    
    #print('Querying Twitter...\n')
    # Each word in the lexicon has scores for:
    # 1)     polarity: negative vs. positive    (-1.0 => +1.0)
    # 2) subjectivity: objective vs. subjective (+0.0 => +1.0)
    # 3)    intensity: modifies next word?      (x0.5 => x2.0)
    for tweet in limit_handled(tweepy.Cursor(api.search, q=text, result_type="recent", lang="en").items(limit)):
        analysis = TextBlob(tweet.text)
        
        if analysis.sentiment.polarity >= threshold:
            polarity_flag = 1
            pos_tweets += 1
        else:
            polarity_flag = 0
            neg_tweets += 1
        
        tweets.append({'created_at': tweet.created_at,
                       'polarity': analysis.sentiment.polarity,
                       'subjectivity': analysis.sentiment.subjectivity,
                       'sentiment': polarity_flag,
                       'tweet': beautify_tweet(tweet.text)})
    if pos_tweets > neg_tweets:
            Overall_Positive = pos_tweets
    else:
            Overall_Negative = neg_tweets
    

    # Create bag of words. Making tweets into vectors. max_features 5 ratio
    vector_tweets = create_vector_of_tweets(tweets, int(limit/5))
    
    # Train and predict using models
    predict_tweets(vector_tweets, limit)
    
    return

# Maintains twitter api threshold
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            
            time.sleep(15 * 60)

def beautify_tweet(raw_tweet):
    # Function to convert a raw tweet to a string of words
    # The input is a single string (a raw tweet), and
    # the output is a single string (a preprocessed tweet)
    #
    # 1. Remove HTML
    tweet_text = BeautifulSoup(raw_tweet, "lxml").get_text()
    #
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z] @[A-Za-z0–9]+ RT[\s]+ https?:\/\/\S+",      # The patttern to search for
                          " ",              # The pattern to replace it with
                          tweet_text)       # The text to search
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #    a list, so convert the stop words to a set
    # stops = set(stopwords.words("english"))
    #
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stopwords.words("english")]

    #
    # 6. Join the words back into one string separated by space,
    #    and return the results.
    return( " ".join( meaningful_words ))

def create_vector_of_tweets(tweets, max_features=100):
    
    clean_train_tweets = []
    for tweet in tweets:
        clean_train_tweets.append(tweet['tweet'])
        
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=max_features)
    
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_tweets)
    
    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()
    
    for i in range(0, len(train_data_features)):
        tweets[i]['tweet'] = train_data_features[i]
    
    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)
    
    # For each, print the vocabulary word and the number of times it
    # appears in the training set
    
    vocab = vectorizer.get_feature_names()
    #print("Count  Word")
    for tag, count in zip(vocab, dist):
        count = count 
        tag = tag
    
    
    return tweets ,tag , count


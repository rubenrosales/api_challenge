from flask import Flask, jsonify, request
import requests
import twitter
import json
import re
import urlparse
from app import app
import ConfigParser
import time
class TweetRc(object):
    def __init__(self):
        self._config = None
    
    def GetConsumerKey(self):
        return self._GetOption('consumer_key')
    
    def GetConsumerSecret(self):
        return self._GetOption('consumer_secret')
    
    def GetAccessKey(self):
        return self._GetOption('access_key')
    
    def GetAccessSecret(self):
        return self._GetOption('access_secret')
    
    def _GetOption(self, option):
        try:
            return self._GetConfig().get('Tweet', option)
        except:
            return None
    def _GetConfig(self):
        if not self._config:
            self._config = ConfigParser.ConfigParser()
            configFilePath = r'twitter/secrets.cfg'
            self._config.read(configFilePath)
        return self._config


rc = TweetRc()

##Establish connection to python-twitter api##
api = twitter.Api(consumer_key=rc.GetConsumerKey(),
                  consumer_secret=rc.GetConsumerSecret(),
                  access_token_key=rc.GetAccessKey(),
                  access_token_secret=rc.GetAccessSecret())


## Format hashtags and mentions (@) into proper urls ##
def format_url(format_as, text):
    user_url = '<a href="https://twitter.com/{0}">@{0}</a>'
    hash_url = '<a href="https://twitter.com/hashtag/{0}">#{0}</a>'
    
    if format_as == 'user':
        url = user_url.format(text)
    elif format_as == 'hashtag':
        url = hash_url.format(text)
    
    return url

## Helper function to format urls ##
def expand_url(short, expanded):
    return '<a href="{0}">{1}</a>'.format(expanded,short)

## replace links in tweet with 'display_url' and link it to it's 'expanded_url' ##
def replace_url(url, status):
    for short,expanded in url.items():
        status = status.replace(str(short), expand_url(str(short),str(expanded)))
    return status

## replace media link with 'display_url' and link it to it's 'expanded_url' ##
def replace_media(url, status):
    for k, v in url.items():
        status = status.replace(str(k), expand_url(str(v[0]),str(v[1])))
    return status

## add links to user profile mentioned in tweet  ##
def replace_usernames(usernames, status):
    for user_name in usernames:
        status = status.replace('@{0}'.format(user_name), format_url('user', user_name))
    return status

## add links to hashtag mentioned in tweet  ##
def replace_hashtags(hashtags, status):
    for hashtag in hashtags:
        status = status.replace('#{0}'.format(hashtag), format_url('hashtag', hashtag))
    return status

## modify N amount of tweets  ##
## N = count user entered ##
def sort_recent_tweets(tweets, count=1):
    keys = sorted(tweets.keys(), reverse=True)
    
    statuses = []
    for index, key in enumerate(keys):
        if index == count:
            break
        status = tweets[keys[index]]['status']
        user = tweets[keys[index]]['user']

        status = replace_url(tweets[keys[index]]['urls'],status)
        status = replace_media(tweets[keys[index]]['media'],status)
        status = replace_usernames(tweets[keys[index]]['user_mentions'],status)
        status = replace_hashtags(tweets[keys[index]]['hashtags'],status)
        
        statuses.append({'status': status, 'user': user})

    return keys[0], statuses

## check if screen name user entered is valid ##
## if it is then it will return N amount of tweets from that user ##
## N = count ##
def verify_user(screen_name, count=1, cursor=None):
    try:
        user = api.GetUserTimeline(screen_name=screen_name, count=count, since_id=cursor)
    except:
        return {}
    else:
        return get_status(user, screen_name)

## get tweets for each user entered ##
def get_status(user, screen_name):
    
    tweets = {}
    
    ## for every tweet, extract and store url, media, hashtags, user mention, ##
    ## and text fields for future manipulation ##
    for index, tweet in enumerate(user):
        
        t = json.loads(str(tweet))
        
        user_mentions, hashtags, urls, media = [], [], {}, []
        single = {}
        
        ##if it contains links then extract it ##
        if 'urls' in t:
            urls = t['urls']

        ## if it contains media then create a dict entry with url as key and ##
        ## tuple of display_url and expanded_url as value ##
        ## so the url in the tweet can be replaced with display_url and expanded_url ##
        if 'media' in t:
            for i in range(0,len( t['media'])):
                single[str(t['media'][i]['url'])] = (str(t['media'][i]['display_url']),str(t['media'][i]['expanded_url']))
            
        for user in tweet.user_mentions:
            user_mentions.append(user.screen_name)

        if 'hashtags' in t:
            hashtags = t['hashtags']

        tweets.update({tweet.id: {'status': tweet.text.encode('utf-8'), 'user': screen_name, \
                        'user_mentions': user_mentions, 'hashtags': hashtags, 'urls': urls, 'media':single}})
    return tweets

@app.route('/statuses', methods=["GET"])
def index():
    
    ## dictionary to hold statuses user requested ##
    statuses = {'next_cursor': 'null', 'statuses': []}
    placeholder = {}
    
    ## parse count and next_cursor from url ##
    if request.args.get('count'):
        count = request.args.get('count')
    else:
        count = 1
    
    if request.args.get('cursor'):
        cursor = int(request.args.get('cursor'))
    else:
        cursor = None
    
    ## for each screen name entered, verify if its valid and return N amount of tweets ##
    ## N = count ##
    if request.args.get('screen_names'):
        for user in request.args.get('screen_names').split(','):
            placeholder.update(verify_user(user, count, cursor))

    ## set tweets and next_cursor for output ##
    if len(placeholder) > 0:
        next_cursor, status = sort_recent_tweets(placeholder, int(count))
        statuses.update({'next_cursor': next_cursor, 'statuses': status})

    return jsonify(statuses)


if __name__ == '__main__':
    app.debug = True
    app.run()

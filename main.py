from tweety import Twitter
import json
import discord_webhook
from datetime import datetime
import os

Config = {
    "Username": "",
    "Webhook_URL": "",
    "Message": "",
}

class Config:
    def __init__(self, path:str) -> None:
        self.path = path
        if not os.path.exists(self.path):
            self.data = Config
            json.dump(self.data, open(self.path, "w"))
        else:
            self.data = json.load(open(self.path, "r"))

    def get(self, key:str) -> any:
        return self.data[key]
    
    def set(self, key:str, value:any):
        self.data[key] = value
        self.save()

    def save(self):
        json.dump(self.data, open(self.path, "w"))

def get_tweets(username:str) -> list:
    twitter = Twitter("session")
    tweets = twitter.get_tweets(username, pages=10)
    return list(tweets)

def sort_tweets(tweets:list) -> list:
    for tweet in tweets:
        if not isinstance(tweet['created_on'], datetime):
            tweet['created_on'] = datetime.strptime(tweet['created_on'], "%Y-%m-%d %H:%M:%S")
    tweets.sort(key=lambda x: x['created_on'], reverse=True)
    return tweets

if __name__ == "__main__":
    config = Config("config.json")
    username = config.get("Username")
    tweets = get_tweets(username)
    tweets = sort_tweets(tweets)
    # for tweet in tweets:
    #     print(tweet['created_on'])
    print(tweets[0])
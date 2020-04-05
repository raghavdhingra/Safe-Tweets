from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers
import json
import twitter_scraper as ts
import numpy as np
import pandas as pd
from textblob import TextBlob
from rest_framework.views import APIView
import re
import os
import pickle as pkl
import warnings
import tweepy
warnings.simplefilter('ignore')
from blacknet.settings import BASE_DIR
from .models import SuspectList

consumer_key = "ri2JedD578SUg4ZUPhvzdAwYg"
consumer_secret = "EmDtL89j5e1DvBgth0BbN7qmfBuV23IxGIf1oGoUOWfOyzWX2D"
access_token = "947748540532498432-no5SFmH3a50FRFMTNHRbzjBr00H9Qvv"
access_token_secret = "NNGTM7gJrHRtD46tQwM07QpAE54hh553p5NzzokdsEGlH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
# Create your views here.
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity

def get_profile(request,username):
  context = ts.Profile(username).to_dict()
  return JsonResponse(context,safe=False)

def hate_speech_detection(tweet):
    # loaded_model = pkl.load(open("/static/approach_1.sav", 'rb'))
    loaded_model = pkl.load(open(os.path.join(BASE_DIR, 'approach_1.sav'), 'rb'))
    ans = loaded_model.predict([clean_tweet(tweet)])
    if ans == [1]:
        return "Offensive"
    if ans == [0]:
        return "Non-Offensive"

def profile_hatespeech_analyzer(keyword):
    tweet_data = []
    for tweet in ts.get_tweets(keyword):
        tweet_data.append(tweet)

    df = pd.DataFrame(data = [tweet['time'] for tweet in tweet_data], columns=["time"])
    df['isRetweet'] = pd.DataFrame([tweet['isRetweet'] for tweet in tweet_data])
    df['text'] = np.array([tweet['text'] for tweet in tweet_data])
    df['replies'] = np.array([tweet['replies'] for tweet in tweet_data])
    df['retweets'] = np.array([tweet['retweets'] for tweet in tweet_data])
    df['likes'] = np.array([tweet['likes'] for tweet in tweet_data])
    df['sentiment_polarity'] = np.array([sentiment(tweet) for tweet in df['text']])
    df['offensive_or_not'] = np.array([hate_speech_detection(tweet) for tweet in df['text']])
    # return [[df.loc[idx,"time"],df.loc[idx,"isRetweet"],df.loc[idx,"text"],
    #         df.loc[idx,"replies"],df.loc[idx,"retweets"],df.loc[idx,"likes"],
    #         df.loc[idx,"sentiment_polarity"],df.loc[idx,"offensive_or_not"]] 
    #         for idx in df.index]
    return df

def profile_hashtag_analyzer(keyword):
    tweets = []
    for tweet in tweepy.Cursor(api.search, q="{} -filter:retweets".format(keyword),tweet_mode='extended',lang="en",since="2020-01-31", until="2020-02-06").items(10):
        tweets.append([tweet.created_at, tweet.user.profile_image_url,
                tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count,
                tweet.in_reply_to_screen_name,tweet.full_text, tweet.favorite_count,tweet.retweet_count])
    df = pd.DataFrame(tweets,columns=["time","profile_img_url","username","followers_count","following_count","reply_to","text","likes","retweet_count"])
    df['sentiment_polarity'] = np.array([sentiment(tweet) for tweet in df['text']])
    df['offensive_or_not'] = np.array([hate_speech_detection(tweet) for tweet in df['text']])
    return df

def TwitterHashTagProcess(hashtag):
    df = profile_hashtag_analyzer(hashtag)
    df = df.to_json(orient='index')
    df = json.loads(df)
    tweet_arr = []
    for i in df:
        tweet_arr.append(df[i])
    # print(df)
    return json.dumps(tweet_arr)

def TwitterUserNameProcess(userName):
    df = profile_hatespeech_analyzer(userName)
    df = df.to_json(orient='index')
    df = json.loads(df)
    tweet_arr = []
    for i in df:
        tweet_arr.append(df[i])
    return json.dumps(tweet_arr)

def home(request):
    if request.method == "POST":
        page = request.POST.get("page_request")
        if page == "twitter":
            return redirect("/api/twitter")
    context = {}
    return render(request,"index.html",context)

def twitterApi(request,userName):
    resp = TwitterUserNameProcess(userName)
    resp = json.loads(resp)
    return JsonResponse(resp,safe=False)

def twitterHashTagApi(request,hashtag):
    resp = TwitterHashTagProcess("#{}".format(hashtag))
    resp = json.loads(resp)
    return JsonResponse(resp,safe=False)

def twitter(request):
    context = {}
    if request.method == "POST":
        resp_Arr = []
        user_input = request.POST.get("usernames")
        user_input = user_input.strip()
        if user_input != "":
            if user_input[:1] == "#":
                twitter_resp_data = TwitterHashTagProcess(user_input)
                context["data1"] = json.loads(twitter_resp_data)
                context["hashtag"] = user_input
                # print(context)
                return render(request,"twitter.html",context)
            else:
                user_List = user_input.split(",")
                for user_name in user_List:
                    user_name = user_name.strip()
                    if user_name != "":
                        # print(user_name)
                        try:
                            twitter_resp_data = TwitterUserNameProcess(user_name)
                            user_profile = ts.Profile(user_name).to_dict()
                            resp_Arr.append({
                                "username":user_name,
                                "data":json.loads(twitter_resp_data),
                                "user_profile":user_profile
                            })
                        except Exception as e:
                            context["error"] = "{}".format(e)
                context["data"] = resp_Arr

        else:
            context["error"] = "Please type a twitter username in the input field."

    return render(request,"twitter.html",context)

def addSuspect(request,username):
    context = {}
    prevList = SuspectList.objects.filter(name="raghav")[0].suspect_list
    if username in prevList:
        context["code"] = 1
        context["response"] = "User already exists"
        return JsonResponse(context,safe=False)
    prevList.append(username)
    SuspectList.objects.filter(name="raghav").update(suspect_list=prevList)
    context["response"] = "{} added to the suspect list".format(username)
    context["code"] = 0
    return JsonResponse(context,safe=False)

def deleteSuspect(request,username):
    context = {}
    prevList = SuspectList.objects.filter(name="raghav")[0].suspect_list
    if username in prevList:
        prevList.remove(username)
        SuspectList.objects.filter(name="raghav").update(suspect_list=prevList)
        context["code"] = 0
        context["response"] = "{} removed from the suspect list".format(username)
    else:
        context["code"] = 1
        context["response"] = "User doesnot exist in the suspect list"
    return JsonResponse(context,safe=False)

class SuspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspectList
        fields = '__all__'

class SuspectListView(APIView):
    def get(self,request):
        member = SuspectList.objects.all()
        serializer = SuspectSerializer(member, many=True)
        return JsonResponse(serializer.data,safe=False)
    def post(self):
        pass

def suspect(request):
    context = {}
    context["data"] = []
    suspect_username = SuspectList.objects.filter(name="raghav")[0].suspect_list
    for user in suspect_username:
        resp = ts.Profile(user).to_dict()
        context["data"].append(resp)
    # print(context)
    return render(request,"suspect.html",context)

#   "/api/twitter/raghav/suspect-list"
#   "for every user there should be an suspect list"
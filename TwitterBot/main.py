import tweepy
import requests
import time
import datetime
import psycopg2
import sys
import json
import random
import twitter
import twitterApi
import fileManager

consumer_token = "6IzigtciQ0wQPhfKQK5a57YWC"
consumer_secret = "qY5b9h3cwY39EYxW6zKIpWteElfTL32pPXYQeg8hqvpzYX639U"
access_token = "2304246030-2V2MbJVRNUXNQB3ixPi0aIZ3YUJx88UhKS3HYxH"
access_token_secret = "ZtGQKu1rUnDFBKytdeu4j0RFthoOS6cO2BSuTXZTwA2zI"

# api = twitter.Api(consumer_key=consumer_token, consumer_secret=consumer_secret, access_token_key=access_token,
# access_token_secret = access_token_secret)

api = twitterApi.set_twitter_api(consumer_token, consumer_secret, access_token, access_token_secret)


def connect_psql():
    # Define our connection string
    conn_string = "host='localhost' dbname='twitter_db' user='kelvin' password='logmein'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)
    conn = 0
    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
    except:
        print "cannot connect to database"

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"


# Get all followers, if someone is not following back after 2 days
def main():
    # Constants.
    search_terms_file = 'search_terms.txt'
    users_file = 'users.json'
    daily_followed_file = 'followed.txt'
    follow_limit = 1000
    max_follow_delay = 70

    followed = fileManager.check_daily_followed(daily_followed_file)
    # update_daily_followed(daily_followed_file)

    print followed

    print "Welcome to 2khc's Twitter bot, search terms from search_terms.txt will be searched for in Twitter" \
          "and users will be followed who tweet with those terms.\n"
    finished = 1
    answer = raw_input("Do you want to enter any search terms? y/n\n")
    if answer == ('y' or 'Y'):
        print "First let's add some search terms. Submit an empty line when done."
        finished = 0
    elif answer == ('n' or 'N'):
        finished = 1

    while (finished == 0):
        search_term = raw_input()
        if search_term == "":
            finished = 1
        else:
            fileManager.add_search_term(search_term)

    while followed < 1000:
        twitterApi.mass_follow(search_terms_file, users_file, daily_followed_file, max_follow_delay)
        followed = fileManager.update_daily_followed(daily_followed_file)


main()

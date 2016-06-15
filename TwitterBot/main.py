import tweepy
import requests
import time
import datetime
import psycopg2
import sys
import json
import random
import twitter

consumer_token = "6IzigtciQ0wQPhfKQK5a57YWC"
consumer_secret = "qY5b9h3cwY39EYxW6zKIpWteElfTL32pPXYQeg8hqvpzYX639U"
access_token = "2304246030-2V2MbJVRNUXNQB3ixPi0aIZ3YUJx88UhKS3HYxH"
access_token_secret = "ZtGQKu1rUnDFBKytdeu4j0RFthoOS6cO2BSuTXZTwA2zI"

api = twitter.Api(consumer_key=consumer_token, consumer_secret=consumer_secret, access_token_key=access_token,
                  access_token_secret=access_token_secret)


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


# connect_psql()

# public_tweets = api.home_timeline()
# for tweets in public_tweets:
#     print tweets

# Search for a user, returns an array of user screen names
# 1 get query
def search_term(term):
    results = api.GetSearch(term)
    users = []
    a = results[0]
    for user in results:
        users.append(user.user.screen_name)
    return users


# Looks up the friendship that you have with a particular user of choice
# 1 get query
def lookup_friendship(screen_name):
    status = api.LookupFriendship(screen_name=screen_name)
    connections = status[0].connections
    return connections


# Get a specified User model
# 1 get query
def search_user(user):
    userModel = api.GetUser(screen_name=user)
    print userModel


# Follows a user, write the user into a json file
def follow_user(json_file, screen_name, is_followed_by):
    follow_date = time.time()
    object = {screen_name: {"following": True,
                            "followed_by": is_followed_by,
                            "follow_date": follow_date}}
    api.CreateFriendship(screen_name=screen_name)
    try:
        with open(json_file) as f:
            data = json.load(f)

        data.update(object)

        with open(json_file, 'w') as f:
            json.dump(data, f)
    except:
        with open(json_file, 'w') as f:
            json.dump(object, f)


# Add a search term to the search_terms.txt file
def add_search_term(search_term):
    try:
        with open('search_terms.txt', 'r+') as f:
            term_exists = False
            for line in f:
                print line
                if line == search_term + '\n':
                    term_exists = True
            if not term_exists:
                f.write(search_term + '\n')
    except:
        with open('search_terms.txt', 'w') as f:
            f.write(search_term)


# Get all search terms in a list
def get_search_terms(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(line.strip())
    print data
    return data


# Remove a search term from the file
def remove_search_term():
    pass


def open_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data


def mass_follow(search_terms_file, users_file, followed_file, maximum_follow_delay):
    terms = get_search_terms(search_terms_file)
    users_json = open_file(users_file)
    count = 0
    for term in terms:
        users = search_term(term)
        for user in users:
            if user in users_json:
                continue
            else:
                connections = lookup_friendship(
                    user)  # of the form {u'muting': False, u'followed_by': False, u'following': False, u'following_received': False, u'blocking': False, u'following_requested': False}
                follow_user(users_file, user, connections['followed_by'])
                update_daily_followed(followed_file)
                print "Followed %s" % user
                count += 1
                time.sleep(random.randrange(maximum_follow_delay - 10, maximum_follow_delay))
    print "Followed %d people." % count


def check_daily_followed(file_name):
    date = datetime.datetime.today()
    now = time.time()
    day = 24 * 60 * 60
    followed = 0
    try:
        with open(file_name, 'r+') as f:
            data = []
            for line in f:
                data.append(float(line.strip()))
            if len(data) == 2:
                if int(data[0]) - now < day:
                    followed = data[1]
                else:
                    print "Length of file is not 2, regenerating..."
                    f.write(str(now) + '\n')
                    f.write(str(followed))
    except:
        with open(file_name, 'w') as f:
            f.write(str(now) + '\n')
            f.write(str(followed))
        print "followed.txt does not exist or has incorrect format. Creating file..."

    return followed


def update_daily_followed(file_name):
    now = time.time()
    day = 24 * 60 * 60
    data = []
    try:
        with open(file_name, 'r+') as f:
            for line in f:
                data.append(float(line.strip()))
                # if data[0] - now > day:
        with open(file_name, 'w') as f:
            for i in range(0, 2):
                if i == 0:
                    f.write(str(data[i]) + '\n')
                else:
                    f.write(str(data[i] + 1))
    except:
        pass


def check_rate_limit(url):
    url = 'https://api.twitter.com/1.1/friendships/create'
    mute_url = 'https://api.twitter.com/1.1/mute'
    status = api.CheckRateLimit(mute_url)
    print status


# Get all followers, if someone is not following back after 2 days
def main():
    # json = {"screen_name": "kelv"}
    search_terms_file = 'search_terms.txt'
    users_file = 'users.json'
    daily_followed_file = 'followed.txt'
    follow_limit = 1000
    max_follow_delay = 70
    followed = check_daily_followed(daily_followed_file)
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
            add_search_term(search_term)

    while followed < 1000:
        mass_follow(search_terms_file, users_file, daily_followed_file, max_follow_delay)
        followed = update_daily_followed(daily_followed_file)

        # mass_follow(search_terms_file, users_file, max_follow_delay)
        # while followed < follow_limit:
        #     pass
        #
        # follow_user(users_file, 'elementalstory', False)


# user = api.get_user('2khch')
# print user.followers_count

main()

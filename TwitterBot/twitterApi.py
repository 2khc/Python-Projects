import twitter
import json
import time
import fileManager
import random

api = twitter.Api()


def set_twitter_api(consumer_token, consumer_secret, access_token, access_token_secret):
    api = twitter.Api(consumer_key=consumer_token, consumer_secret=consumer_secret, access_token_key=access_token,
                      access_token_secret=access_token_secret)
    return api


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


def unfollow_user(json_file, screen_name):
    try:
        with open(json_file, 'r+') as f:
            data = json.load(f)
            if screen_name in data:
                data[screen_name].following = False
                json.dump(data, f)
    except:
        pass


def mass_unfollow(users_file):
    users_json = fileManager.open_file(users_file)
    for user in users_json:


def mass_follow(search_terms_file, users_file, followed_file, maximum_follow_delay):
    terms = fileManager.get_search_terms(search_terms_file)
    users_json = fileManager.open_file(users_file)
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
                fileManager.update_daily_followed(followed_file)
                print "Followed %s" % user
                count += 1
                time.sleep(random.randrange(maximum_follow_delay - 10, maximum_follow_delay))
    print "Followed %d people." % count


def check_rate_limit(url):
    url = 'https://api.twitter.com/1.1/friendships/create'
    mute_url = 'https://api.twitter.com/1.1/mute'
    status = api.CheckRateLimit(mute_url)
    print status

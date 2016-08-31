"""
Simple example of querying Elasticsearch creating REST requests
"""
import requests
import json
import time
import pyperclip
import winsound
import threading
import concurrent.futures
import ConfigParser
# import futures
import codecs


def build_query(term, max_price, min_price, fully_linked, corrupted, time_s, ):
    query = {}

    if fully_linked == True:
        query = json.dumps({
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"info.name": {"value": term}}},
                                {"term": {"shop.hasPrice": {"value": True}}},
                                {"term": {"attributes.league": {"value": "Prophecy"}}},
                                {"term": {"attributes.corrupted": {"value": corrupted}}},
                                {"term": {"sockets.largestLinkGroup": {"value": 6}}},
                                {"range": {"shop.chaosEquiv": {"lte": max_price,
                                                               "gte": min_price}}},
                                {"range": {"shop.updated": {"gte": int(time_s)}}}
                            ]
                        }
                    }
                }
            },
            "aggs": {
                "NAME": {
                    "terms": {
                        "field": "info.fullName",
                        "size": 100
                    }
                }
            },
            "size": 10
        })
    elif fully_linked == False:
        query = json.dumps({
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"info.name": term}},
                                {"term": {"shop.hasPrice": {"value": True}}},
                                {"term": {"attributes.league": "Prophecy"}},
                                {"term": {"attributes.corrupted": corrupted}},
                                {"range": {"shop.chaosEquiv": {"lte": max_price,
                                                               "gte": min_price}}},
                                {"range": {"shop.updated": {"gte": int(time_s)}}}
                            ]
                        }
                    }
                }
            },
            "aggs": {
                "NAME": {
                    "terms": {
                        "field": "info.fullName",
                        "size": 100
                    }
                }
            },
            "size": 10
        })

    # query = json.dumps({
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 {"range": {
    #                     "shop.updated": {
    #                         "gte": "now-1d"
    #                     }
    #                 }},
    #                 {"term": {"info.fullName": "The Gambler"}},
    #                 {"term": {
    #                     "attributes.baseItemType": {
    #                         "value": "Card"
    #                     }
    #                 }},
    #                 {"term": {
    #                     "shop.hasPrice": {
    #                         "value": "true"
    #                     }
    #                 }},
    #                 {"term": {
    #                     "attributes.league": {
    #                         "value": "Prophecy"
    #                     }
    #                 }}
    #             ]
    #         }
    #     },
    #     "aggs": {
    #         "NAME": [
    #             {"terms": {
    #                 "field": "info.fullName",
    #                 "size": 100
    #             }},
    #             {"terms": {
    #                 "field": "shop.chaosEquiv",
    #                 "size": 100
    #             }}
    #         ]
    #     },
    #     "size": 0
    # })
    # query = json.dumps({
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 {"range": {
    #                     "shop.updated": {
    #                         "gte": "now-7d/d"
    #                     }
    #                 }},
    #                 {"term": {"info.fullName": "The Gambler"}},
    #                 {"term": {
    #                     "attributes.baseItemType": {
    #                         "value": "Card"
    #                     }
    #                 }},
    #                 {"term": {
    #                     "shop.hasPrice": {
    #                         "value": "true"
    #                     }
    #                 }},
    #                 {"term": {
    #                     "attributes.league": {
    #                         "value": "Prophecy"
    #                     }
    #                 }}
    #             ]
    #         }
    #     },
    #     "aggs": {
    #         "name": {
    #             "terms": {
    #                 "field": "info.fullName",
    #                 "size": 200,
    #                 "order": {
    #                     "percentiles.25": "desc"
    #                 }
    #             },
    #             "aggs": {
    #                 "percentiles": {
    #                     "percentiles": {
    #                         "field": "shop.chaosEquiv",
    #                         "percents": [
    #                             25
    #                         ]
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     "size": 0
    # })
    return query


def build_message(hit):
    message = "@%(username)s Hi, I would like to buy your %(item_name)s for %(amount)s %(currency_type)s in Prophecy (stash tab %(tab)s)" % \
              {"username": hit['_source']['shop']['lastCharacterName'], "item_name": hit['_source']['info']['name'],
               "amount": hit['_source']['shop']['amount'],
               "currency_type": hit['_source']['shop']['currency'],
               "tab": hit['_source']['shop']['stash']['stashName']}

    pyperclip.copy(message)
    # return message


def search(uri, term, max_price, min_price, fully_linked, corrupted, time_s):
    query = build_query(term, max_price, min_price, fully_linked, corrupted, time_s)
    # query = json.dumps({
    #     "query": {
    #         "filtered": {
    #             "filter": {
    #                 "bool": {
    #                     "must": [
    #                         {"term": {"info.name": term}},
    #                         {"term": {"shop.hasPrice": {"value": True}}},
    #                         {"term": {"attributes.league": "Prophecy"}},
    #                         # {"term": {"shop.verified": {"value": "YES"}}},
    #                         {"range": {"shop.chaosEquiv": {"lte": max_price}}},
    #                         {"range": {"shop.updated": {"gte": int(time_s)}}}
    #                     ]
    #                 },
    #
    #             }
    #         }
    #     },
    #     "aggs": {
    #         "NAME": {
    #             "terms": {
    #                 "field": "info.fullName",
    #                 "size": 100
    #             }
    #         }
    #     },
    #     "size": 10
    # })
    try:
        response = requests.get(uri, data=query)
        results = json.loads(response.text)

        process_results(results, 500)
        # print "SUCCESS"
    except:
        print "Temporarily blocked for requesting too fast."

        # return results


def process_results(results, max_price):
    if results['hits']['hits']:

        for hit in results['hits']['hits']:

            if ('sockets' in hit['_source']) and hit['_source']['sockets']['largestLinkGroup'] == 6 and \
                            hit['_source']['attributes']['corrupted'] == False:
                build_message(hit)
                print hit['_source']['info']['name'] + " " + hit['_source']['shop'][
                    'lastCharacterName'] + " " + str(
                    hit['_source']['shop']['chaosEquiv']) + " " + hit['_source']['shop'][
                          'defaultMessage'] + " " + str(
                    hit['_source']['shop']['updated'])
                winsound.Beep(400, 1000)
            elif 'sockets' not in hit['_source']:
                print hit['_source']['info']['name'] + " " + hit['_source']['shop'][
                    'lastCharacterName'] + " " + str(
                    hit['_source']['shop']['chaosEquiv']) + " " + hit['_source']['shop'][
                          'defaultMessage'] + " " + str(
                    hit['_source']['shop']['updated'])
                build_message(hit)
                winsound.Beep(400, 1000)
                # else:
                #     print "Nothing found"

                # print json.dumps(results, sort_keys=False, indent=4, separators=(',', ': '))


def get_items():
    # items = [
    #     ['From The Void', 115],
    #     ['Voidheart', 120],
    #     ['The Brittle Emperor', 136],
    #     ["Voll\'s Protector", 400]
    # ]

    i = [
        {
            "name": "From The Void",
            "chaosEquiv": 128,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": False
        },
        {
            "name": "Voidheart",
            "chaosEquiv": 144,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": False
        },
        {
            "name": "Voll\'s Protector",
            "chaosEquiv": 376,
            "minPrice": 2,
            "fullyLinked": True,
            "corrupted": False
        },
        {
            "name": "Kaom\'s Heart",
            "chaosEquiv": 184,
            "minPrice": 2,

            "fullyLinked": False,
            "corrupted": False
            
        },
        {
            "name": "Kaom\'s Heart",
            "chaosEquiv": 184,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": True
        },
        {
            "name": "Shavronne\'s Wrappings",
            "chaosEquiv": 540,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": False
        },
        {
            "name": "Void Battery",
            "chaosEquiv": 328,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": False
        },
        {
            "name": "Voll\'s Devotion",
            "chaosEquiv": 960,
            "minPrice": 2,
            "fullyLinked": False,
            "corrupted": True
        }
    ]

    return i


if __name__ == '__main__':
    # print "hio"
    # config = ConfigParser.SafeConfigParser()
    # config.read('config.cfg')
    # try:
    #     if config.get('settings','first-run') == False:
    #         print "Time to build config"
    # except:
    #     config.add_section('settings')
    #
    # with open('config.cfg', 'wb') as configfile:
    #     config.write(configfile)

    # temp_time = time.time()
    print time.time()
    print "sdkfjwer"

    uri_search = 'http://api.exiletools.com/index/_search'

    items = get_items()
    num_of_items = len(items)
    # num_of_items = len(items.keys())

    while True:
        temp_time = time.time() * 1000 - 48000

        # threads = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(num_of_items):
                # t = threading.Thread(target=search, args=(uri_search, items[i][0], items[i][1], temp_time))
                # threads.append(t)
                future = executor.submit(search, uri_search, items[i]['name'], items[i]['chaosEquiv'],
                                         items[i]['minPrice'],
                                         items[i]['fullyLinked'], items[i]['corrupted'], temp_time)
                # t.start()
                time.sleep(0.2)

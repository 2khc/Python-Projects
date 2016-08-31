import time
import json

def check_daily_followed(file_name):
    # date = datetime.datetime.today()
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


# Remove a search term from the file
def remove_search_term():
    pass


def open_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data


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

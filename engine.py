import json
from random import shuffle


#utils funtions
def load_json(file_name):
    contents = open("data/%s" % file_name, 'r').read()
    return json.loads(contents)

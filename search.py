#!/usr/bin/python

from requests import Session
import sys
import getopt
import json

URL_INDEX = "http://localhost:9200/code/"
URL_SEARCH = URL_INDEX + "_search"


def search(match):

    fields = ["path"]
    query = {}
    query['fields'] = fields
    query['query'] = {"term": match}
    s = Session()
    r = s.get(URL_SEARCH, data=json.dumps(query))
    return r.text


if __name__ == "__main__":

    argv = sys.argv[1:]
    match = {}
    try:
        opts, args = getopt.getopt(
            argv, "hl:s:n", ["language=", "source=", "filename="]
        )
        for opt, arg in opts:
            if opt == '-h':
                print 'search.py -l <language> -s <source> -n <filename>'
                sys.exit()
            elif opt in ("-l", "--language"):
                match['language'] = arg
            elif opt in ("-s", "--source"):
                match['source_code'] = arg
            elif opt in ("-n", "--filename"):
                match['filename'] = arg

        json_resp = search(match)
        response = json.loads(json_resp)
        hits = response['hits']
        for hit in hits['hits']:
            item = hit['fields']
            path = item['path']
            print path[0]

    except getopt.GetoptError:
        print 'search.py -l <language> -s <source> -n <filename>'

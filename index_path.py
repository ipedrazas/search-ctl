#!/usr/bin/python

import os
from sys import argv
import ntpath
import requests
import hashlib
import json


FORMATS = ['py', 'html', 'java', 'go', 'htm', 'css', 'rb', 'md', 'txt']

URL_INDEX = "http://localhost:9200/code/"
URL_TYPE = URL_INDEX + "source_file/"


def read_file(file):
    try:
        txt = open(file)
        return txt.read()
    except:
        print "Boom"
        return None


def list_files(dir):
    r = []
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:
        files = os.walk(subdir).next()[2]
        if (len(files) > 0):
            for file in files:
                if not os.path.isdir(file):
                    r.append(subdir + "/" + file)
    return r


def is_indexable(file_format):
    return file_format in FORMATS


def get_format(file):
    if "." in file:
        pos = file.index(".")
        return file[pos + 1:]


def get_file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def process_file(file):
    format = get_format(file)
    if is_indexable(format):
        raw = read_file(file)
        if raw:
            doc = {}
            doc['source_code'] = read_file(file)
            doc['path'] = file
            doc['file_name'] = get_file_name(file)
            doc['language'] = get_format(file)
            m = hashlib.md5()
            m.update(file)
            doc['_id'] = m.hexdigest()
            return doc
    return None


def post_object(obj):
    try:
        r = requests.put(URL_TYPE + obj['_id'], json.dumps(obj))
        print obj['path'] + " " + r.text
    except Exception, e:
        print e


script, filename = argv

files = list_files(filename)


for f in files:
    obj = process_file(f)
    if obj:
        post_object(obj)

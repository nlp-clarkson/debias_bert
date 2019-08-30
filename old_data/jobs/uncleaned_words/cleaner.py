#!/usr/bin/env python3

#obtain paths of a file
import pathlib
from pathlib import Path

import json

#create path object for input dir
features_dir = Path('.')

#Function that gets the tokens of the word
token = {}
#find all .jsonl files in features_dir
for path in features_dir.glob('bookkeeper.jsonl'):
    print("in loop")
    #convert path obj to str
    str_path = str(path)
    print('idsdsdsds%s' % str_path)


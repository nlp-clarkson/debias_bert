#!/usr/bin/env python3

import pprint
from pprint import pprint

# Could get paths of a file
import pathlib
from pathlib import Path

import json

import numpy as np

# create path object for input dir
features_dir = Path('.')

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# PCA library
from sklearn.decomposition import PCA

# our little library :)

#Function that gets the vector & cleans it.
def get_vectors(dir_path):
    token_values = {}
    # find all .jsonl files in features_dir
    for path in features_dir.glob(dir_path):
        # convert path obj to str
        str_path = str(path)

        # debug print out
        print('\n########################')
        print('Starting: %s' % str_path)
        print('########################\n')

        # open the current file & load the json files in a dictionary
        with open(str_path, 'r') as f: 
            # decode json into data variable
            data = json.load(f)

        # iterate over the json data & throw out CLS & SEP
        for feature in data['features']:
            if feature['token'] in ['[CLS]', '[SEP]']:
                continue
            print('Token: %s' % feature['token'])

            # initialize new dict
            token_values[feature['token']] = {}

            # alias new dictionary
            token_dict = token_values[feature['token']]

            # loop over the word vector stuff
            for vector in feature['layers']:
                print('  Index: %d' % vector['index'])
                print('  Values: (%d)' % len(vector['values']))
              
                #stores the token values inside the token_dict, which contains (index & values)
                token_dict[vector['index']] = np.array(vector['values'])

                # loop over each value in hidden layer values
                for n in vector['values']:
                    print('    %f' % n)
    return token_values

debug_vectors = get_vectors('debug/*.jsonl')

for token, indices in debug_vectors.items():
    for index, values in indices.items():
        print(index, values)
        break
    break

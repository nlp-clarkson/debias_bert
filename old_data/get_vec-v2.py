#!/usr/bin/env bash

import sys

import pathlib
import json

import math
from math import cos

import sklearn
from sklearn.decomposition import PCA

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

from pprint import pprint

APP = {
    'pronouns_input_dir': 'pronouns',
    'pronouns_output_dir': 'pronouns_vectors',
    'jobs_input_dir': 'test',
    'jobs_output_dir': 'fixed_vectors',
    'verbose': False
}

def search_dir(input_dir, regex):
    path_obj = pathlib.Path(input_dir)

    file_list = []
    for path in path_obj.glob(regex):
        file_list.append(path)
    return file_list

def get_vectors(file_list):
    vector_dict = {}
    bad_tokens = ['[CLS]', '[SEP]']

    for i, path in enumerate(file_list, start=1):
        token_dict = {}

        name = path.stem
        if APP['verbose']:
            print('* Adding %s (%d)' % (name, i))
        with open(path, 'r') as f:
            data = json.load(f) # decode json into dictionary

            for feature in data['features']:
                token = feature['token']
                # check if it is a token we want to ignore
                if token in bad_tokens:
                    continue # skip bad tokens
                # check if tokens already exists
                if token in token_dict:
                    if APP['verbose']:
                        print('  Warning: %s already exists in token_dict!' % token)
                if APP['verbose']:
                    print('  + %s' % token)
                token_dict[token] = {}
                token_dict_alias = token_dict[token]

                for vector in feature['layers']:
                    token_dict_alias[vector['index']] = np.array(vector['values'])
        if name in vector_dict:
            print('  Warning: %s already exists in vector_dict!' % name)
        vector_dict[name] = token_dict
    return vector_dict

def cat_indices(vector):
    cat = np.add(vector[-1], vector[-2])
    cat = np.add(cat, vector[-3])
    cat = np.add(cat, vector[-4])
    print('Debug: %d' % len(cat))
    return cat

def cat_vectors(token_dict):
    tmp_vec = np.zeros(768)
    for token, indices in token_dict.items():
        tmp_vec = np.add(tmp_vec, indices['cat'])
    return tmp_vec


def calc_g_direction(pronoun_dict):
    #female & male lists of pronouns
    female_words = ['she','her','woman','Mary','herself','daughter','mother','gal','girl','female']
    male_words = ['he','his','man','John','himself','son','father','guy','boy','male']

    matrix = []
    my_vec = lambda key: pronoun_dict[key]['cat']
    for male, female in zip(male_words, female_words):
        center = (my_vec(male) + my_vec(female))/2
 
        matrix.append(my_vec(male) - center)
        matrix.append(my_vec(female) - center)
    pca = PCA(n_components=10)
    pca.fit(matrix)
    return pca.components_[0], pca.explained_variance_ratio_

def calc_direct_bias(vector_dict, g):
    N = len(vector_dict)
    c = 1 # how strict we want the bias measuring to be
    sum_ = 0.0
    for sentence, token_dict in vector_dict.items():
        sum_ += abs(np.cos(token_dict['cat'], g))**c
    direct_bias = (1/N)*sum_
    return direct_bias

def man_is_to_woman(input_dir, output_dir):
    file_list = search_dir(input_dir, '*.jsonl')

    vector_dict = get_vectors(file_list)
    
    # loop through each vectors in the dictionary
    for sentence, token_dict in vector_dict.items():
        if APP['verbose']:
            print('* Starting %s' % sentence)

        # concatenate the token's indices
        for token, indices in token_dict.items():
            if APP['verbose']:
                print("  * Concatenating %s's indices" % token)
            indices['cat'] = cat_indices(indices)

        # concentate the concatenated indices of all the tokens
        if APP['verbose']:
            print("  * Concatenating %s's tokens" % sentence)

        token_dict['cat'] = cat_vectors(token_dict)
        
    return vector_dict

def main():
    jobs_dict = man_is_to_woman(APP['jobs_input_dir'], APP['jobs_output_dir'])
    pronouns_dict = man_is_to_woman(APP['pronouns_input_dir'], APP['pronouns_output_dir'])
    g, evr = calc_g_direction(pronouns_dict)
    direct_bias = calc_direct_bias(jobs_dict, g)
    #n = 10
    #plt.bar(range(n), evr)
    #plt.xticks(range(n),range(10))
    #plt.show()
    

if __name__ == '__main__':
    main()

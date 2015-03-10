__author__ = 'fabienngo'

import os
import glob
import json

with open('../res/mots_vides_grand.txt', 'r') as file:
    stop_word_set = set(file.readlines())
stop_word_set = {el[:-1] for el in stop_word_set}

path_1 = '../res/indices/rtbf_info_index_08.03.2015'
path_2 = '../res/indices/rtbf_info_index_08032015'

vocabulary_set = set()
for infile in glob.glob(os.path.join(path_1, '*.json')):
    with open(infile, 'r') as file:
        try:
            doc = json.load(file)['keywords']
            for el in doc:
                vocabulary_set.add(el)
        except:
            pass

for infile in glob.glob(os.path.join(path_2, '*.json')):
    with open(infile, 'r') as file:
        try:
            doc = json.load(file)['keywords']
            for el in doc:
                vocabulary_set.add(el)
        except:
            pass

print(len(vocabulary_set))

vocabulary_set

s = "Chemin de fer"
s.replace(" ", "_")
with open('../res/keywords_.txt', 'a') as f:
    for keyword in vocabulary_set:
        s = keyword.replace(" ", "_")
        f.write(keyword + "\n")
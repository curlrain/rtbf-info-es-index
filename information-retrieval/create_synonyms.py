__author__ = 'fabienngo'


import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
DBPEDIA_PATH = "http://fr.dbpedia.org/page/"


def find_synonyms(word):
    synonyms = []
    try:
        connexion = requests.get(DBPEDIA_PATH + word)
        soup = BeautifulSoup(connexion.text)
        for el in soup.find_all('a', rev="dbpedia-owl:wikiPageRedirects"):
            synonyms.append(el.contents[1][1:])
        print(len(synonyms))
    except:
        print("zut")
        pass
    return synonyms
with open('res/keywords_.txt', 'r') as file:
    keywords = [keyword[:-1] for keyword in file.readlines()]

# type(keywords)
# find_synonyms("chaussure".title())


synonyms_dict = {keyword.replace("_", " "): find_synonyms(keyword.title()) for keyword in keywords}
print("done")

json_string = json.dumps(synonyms_dict, indent=4)

with open('res/raw_synonyms.json', 'w') as f:
    f.write(json_string)



with open('res/raw_synonyms.json', 'r') as f:
    synonyms_dict = json.load(f)


synonyms_list = [", ".join(v + [k]) for k, v in synonyms_dict.items() if v != []]
len(synonyms_list)
synonyms_list




with open('res/rtbf-info-syn.text', 'a') as f:
    for el in synonyms_list:
        f.write(el + "\n")
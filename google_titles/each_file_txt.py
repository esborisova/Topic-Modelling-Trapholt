import json
import pandas as pd
import spacy
import re
import codecs
import sys
import pathlib
from pathlib import Path
import os



def load_data(path: str, argument):

    new_path = os.path.join(path, argument)
    
    with open(new_path, encoding = 'utf-8') as f:
        dataset = json.load(f)
    return dataset

 
def extract_title(dataset: pd.DataFrame) -> list:
    titles = []
    for i in dataset['Browser History']:
            try:
                 titles.append(i['title'])
            except KeyError:
                    pass
    return titles

def remove_after_dot(argument):
    sep = '.'
    argument = argument.split(sep, 1)[0]
    return argument


def create_txt(dataset: list, argument, path):

    argument = remove_after_dot(argument)
    argument = argument + '.txt'

    new_path = os.path.join(path, argument)
    f = open(new_path, 'w')
    
    for item in dataset:
        without_line_breaks = item.replace("\n", " ")
        without_line_breaks = without_line_breaks.replace("\r", " ")
        lines = without_line_breaks + "\n"
        f.write(lines)
    f.close()


data = load_data('JSON_files/', str(sys.argv[1]))

all_titles = extract_title(data)

#my_file = open("sum", "a")
#my_file.write(str(len(all_titles)))
#my_file.write("\n")
#my_file.close()

print(len(all_titles))

create_txt(all_titles, str(sys.argv[1]), 'prepared_txt/')

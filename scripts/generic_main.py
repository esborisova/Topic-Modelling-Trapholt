import sys
import ast
import pathlib
from pathlib import Path
import os
from functions import *
import os
import datetime as dt
import time
import json
import pandas as pd
import spacy
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
import codecs
import pathlib
from pathlib import Path
import os
import gensim
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
from gensim.corpora import Dictionary
import pyLDAvis.gensim_models
import pyLDAvis.sklearn
from sklearn.decomposition import LatentDirichletAllocation


paths = ['../generic_models/FBG_model.txt', '../generic_models/GG_model.txt']

while True:
    for i in paths:
        with open(i) as f:
            data = ast.literal_eval(f.read())
            data = list(data)
            
            bigram, dictionary, corpus = prepare_input(data)

            max_topics = set_max_topics(data)
            min_topics = 2
            step = 2
           
            x = range(min_topics, max_topics, step)
            coherence_values = compute_c_v(dictionary = dictionary, 
                                           corpus = corpus, 
                                           texts = data, 
                                           min_topics = min_topics, 
                                           max_topics = max_topics, 
                                           step = step)
            
            best_result_index = coherence_values.index(max(coherence_values))
            ldamodel = LdaModel(corpus = corpus, 
                                num_topics = x[best_result_index], 
                                id2word = dictionary,
                                update_every = 1,
                                passes = 10,
                                per_word_topics = True)

            model = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
        
            if 'FB' in i:
                model_name = 'FBG_model.html'
            else:
                model_name = 'GG_model.html'
        
            save_model(model, '../html/', model_name)

    time.sleep(72000)

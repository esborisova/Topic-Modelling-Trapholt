import sys
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


nlp = spacy.load("da_core_news_sm")
stops_path = 'stops/FB_stop_words.txt'


while True:
    for file in os.listdir('../json/'): 
        if 'FB' in file:
            print(file)
        
            file_path = os.path.join('../json/', file)
            atime, ago = get_time(file_path)
   
            if atime <= ago:

                stops = open(stops_path,"r+")
                stops = stops.read().split()
            
                file_name = file.split('_')[-1].split('.')[0]

                try:
                    data = load_json(file_path)
                    extracted_posts = extract_posts(data)
                    txt_name = file_name + '.txt'

                    if not os.path.exists('../FB_txt/'):
                        os.mkdir('../FB_txt/')
                    else:
                        pass
    
                    txt_path = os.path.join('../FB_txt/', txt_name)
                    save_txt(extracted_posts, txt_path)
                    decoded_data = decode(txt_path)
                    no_mentions = remove_mentions(decoded_data)
                    no_empty_str = [string for string in  no_mentions if string != ""]
                    no_empty_str = change_letter(no_empty_str)
                    cleaned_data = clean_text(no_empty_str)
                    cleaned_data = [string for string in cleaned_data if string != ""]
                    tokenized_data = tokenize(cleaned_data)
                    lemmatized_data = lemmatize(tokenized_data, nlp = nlp)
                    lemmatized_data = change_char(lemmatized_data)
                    no_stops = remove_stops(lemmatized_data, stops)
                    no_stops = [l for l in no_stops if len(l) != 0]
                    no_stops = rem_single_char(no_stops)

                    bigram, dictionary, corpus = prepare_input(no_stops)

                    max_topics = set_max_topics(no_stops)
                    min_topics = 2
                    step = 2
           
                    x = range(min_topics, max_topics, step)
                    coherence_values = compute_c_v(dictionary = dictionary, 
                                                   corpus = corpus, 
                                                   texts = no_stops, 
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
                    model_name = 'FB_' + file_name + '.html'

                  #  if not os.path.exists('HTML'):
                  #      os.mkdir('HTML/')
                  #  else:
                  #       pass

                    save_model(model, '../html/', model_name)

                    # saving preprocessed data to .txt for generic model 
                    if 'Contribute' in file:
                
                        data_generic = slice_data(no_stops)

                        #if not os.path.exists('../Generic_models/'):
                        #    os.mkdir('../Generic_models/')
    
                        if not os.path.exists('../generic_models/FB_generic.txt'):
                            with open('../generic_models/FB_generic.txt', 'w') as fp:
                                pass

                        txt_append('../generic_models/FB_generic.txt', data_generic)
                                      
                
                except ValueError:  

                    if not os.path.exists('../not_processed/'):
                            os.mkdir('../not_processed/')
                    else:
                        pass
                    old_name = '../json/' + file
                    file_name = file.split('_')[-1]
                    new_name = '../not_processed/' + 'Decoding_JSON_has_failed_' + file_name
                    os.rename(old_name, new_name)
                   
  
            else:
                print('No')
                continue

            if os.path.exists(file_path):
                os.remove(file_path) 

            if os.path.exists('../FB_txt/'+ file_name + '.txt'):
                os.remove('../FB_txt/'+ file_name + '.txt')

    time.sleep(60)
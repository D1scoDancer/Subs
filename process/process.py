import os
import pandas as pd
import numpy as np
import srt
import warnings
import string # for work with strings
import nltk   # Natural Language Toolkit
import sys
import spacy

from .translate import translate


def process(file):
    warnings.filterwarnings("ignore")
    ###
    filepath = file.path
    with open(filepath, encoding='utf-8-sig') as f:
        sub_text = f.read()
    
    ###
    subs = srt.parse(sub_text)

    subs = list(subs)
    for sub in subs:
        sub.content = sub.content.replace('\n', ' ')

    ###
    data = pd.DataFrame()

    for sub in subs:
        df = pd.DataFrame({'start':[sub.start],
                     'end': [sub.end],
                     'content': [sub.content],
                     })
        data = data.append(df)

    ##
    data.reset_index(drop = True, inplace = True)


    ## run tokenization and data cleaning
    texts = process_data(data['content'])

    ##
    data['tokens'] = texts

    ## 
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    lemmas = []
    for tokens in data['tokens']:
        a = []
        for token in tokens:
            doc = nlp(token)
            lemma = " ".join([token.lemma_ for token in doc])
            if lemma == '-PRON-':
                continue
        a.append(lemma)
        lemmas.append(a)

    ##
    data['lemmas'] = lemmas

    ##
    word_freq = pd.read_csv('process/media/process/media/unigram_freq.csv')

    ##
    all_words = []

    ##
    for i in data['lemmas']:
        all_words.extend(i)

    ##
    mapping = pd.DataFrame(all_words, columns=['word'])
    mapping = mapping.drop_duplicates(subset=['word'])
    mapping.reset_index(inplace=True, drop=True)

    ##
    rank = []

    for i in range(0, mapping.shape[0]):
        try:
            rank.append(word_freq.loc[word_freq['word'] == mapping['word'].loc[i]].index[0])
        except:
            rank.append(-1)

    ##
    mapping['rank'] = rank

    ##
    mapping = mapping[mapping['rank'] != -1]

    ##
    mapping = mapping.sort_values(by=['rank'], ascending=False)
    mapping.reset_index(inplace = True, drop = True)
    

    ##  Process completed
 


    ### TRANSLATE
    mapping = mapping.head(100)
    words_to_translate  = list(mapping['word'])
    response = translate(words_to_translate)
    
    translations = []
    for translation in response.json()['translations']:
        translations.append(translation['text'])

    mapping['russian'] = translations

    ### FILE output
    file_name = file.name
    file_name = file_name.split("/")[-1]
    file_name = file_name.rsplit(".", 1)[0] 
    file_name += '.xlsx'

    ### Drop rank column
    mapping.drop(columns = ['rank'], inplace=True)

    ### Rename column
    mapping.rename(columns={"word": "english"}, inplace=True)

    mapping.to_excel(file_name)


def process_data(data):
    # nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')
    word_tokenizer = nltk.WordPunctTokenizer()
    texts = []
    targets = []

    for item in data:
        tokens     = word_tokenizer.tokenize(item) 
        tokens = [word for word in tokens if (word not in string.punctuation and word not in stop_words and not word[0].isupper())]
        
        texts.append(tokens) 
    
    return texts
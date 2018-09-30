# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:56:11 2018

@author: Sachin 
"""

import nltk
import pandas as pd
import numpy as np
import random
import string    #to process standard python strings
import os
os.getcwd()
os.chdir('C:\\MBA\\Projects\\chatbot')

#read text file
f=open('chatbot.txt','r',errors='ignore')
f
raw=f.read()
raw=raw.lower()
#nltk.download('punkt')
#nltk.download('wordnet')

sent_tokens=nltk.sent_tokenize(raw)
word_tokens=nltk.word_tokenize(raw)

sent_tokens[:2]
word_tokens[:10]
lemmer=nltk.stem.WordNetLemmatizer()


def lemtokens(tokens):
    return[lemmer.lemmatize(token) for token in tokens]
remove_puct_dict=dict((ord(punct),None) for punct in string.punctuation)
def lemnormalize(text):
    return lemtokens(nltk.word_tokenize(text.lower().translate(remove_puct_dict)))

greeting_inputs=('Hello','Hi','whats up','hey')
greeting_output=['hi','hello','I am glad u r talking to me!']    


#cheking for greetings
def greetings(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_output)
        
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#generating responce
def response(user_response):
    robo_response=''
    tfidfvec=TfidfVectorizer(tokenizer=lemnormalize,stop_words='english')
    tfidf=tfidfvec.fit_transform(sent_tokens)
    vals=cosine_similarity(tfidf[-1],tfidf)
    idx=vals.argsort()[0][-2]
    flat=vals.flatten()
    flat.sort()
    req_tfidf=flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry"
        return robo_response
    else:
        robo_response=robo_response+sent_tokens[idx]
        return robo_response
    
flag=True
print("BOT: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")

while (flag==True):
    user_response=input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you'):
            flag=False
            print("BOT: u R welcome")
        else:
            if(greetings(user_response)!=None):
                print("BOT: "+greetings(user_response))
            else:
                sent_tokens.append(user_response)
                word_tokens=word_tokens+nltk.word_tokenize(user_response)
                final_words=list(set(word_tokens))
                print("BOT :",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("BOT : Bye")

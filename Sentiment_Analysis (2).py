# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:27:11 2023

@author: 91944
"""
import re
import string

import nltk
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import streamlit as st
from nltk.stem import WordNetLemmatizer

lm= WordNetLemmatizer()
from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()
import pickle


#Text Cleaning
def text_cleaning(Text):

    #removal of the link
    Text = re.sub('https?://\S+|www\.\S+', '', Text)
    #removal of punctuatoins
    punc=str.maketrans(string.punctuation,' '*len(string.punctuation))
    Text=Text.translate(punc)
    #removal of numbers
    Text = re.sub(r'\d+', '', Text)
    #removal of the special characters
    Text=re.sub(r'[^\w\s]', '', Text)
    #lower case transformation
    Text=Text.lower()
    #remove the non-english alphabets
    Text=re.sub(r'[^\u0000-\u007F]+', '', Text)

    return Text

Stopwords = (set(nltk.corpus.stopwords.words("english")))
Stopwords.remove('not')
Stopwords.remove('down')
Stopwords.remove("more")
Stopwords.remove("under")
domain_words=['finnish','russian','finland','russia','swedish','firm','eighteen','months','taking','total','square',
              'eur','million','announcement','day','earlier','glaston','net','third','quarter','dropped','mln','euro',
              'period','april','baltic','countries','eur mn','last','year','million','state',
              'office','msft','orcl','goog','crm','adbe','aapl','afternoon','esi','billion','eurm','third','quarter',
              'half','annually','annualy','first','second','nine','helsinki','omx','year','month','day','indian','india','third'
              ,'fourth','mn','mln','in','eur','euro','months','goods','one','the', 'of', 'in', 'to', 'and', 'a','eur', 'for',
              's', 'is', 'on', 'from', 'will', 'company', 'as', 'mn', 'its', 'with', 'by', 'be', 'has', 'at','it', 'said',
              'million', 'net', 'year', 'm', 'that', 'was', 'group', 'an', 'mln','new', 'are', 'quarter','this', 'oyj','also',
              'have', 'which', 'first', 'euro', 'today', 'been', 'about', 'helsinki', 'per','total', 'after', 'nokia', 'bank',
              'based', 'were', 'we', 'than', 'some','or', 'other', 'all', 'one', 'hel' ,'our', 'plc', 'now', 'last', 'their',
              'second', 'ceo', 'pct', 'january', 'into', 'aapl', 'would', 'eurm', 'out', 'part', 'oy','i','september', 'usd',
              'two', 'third','earlier', 'can', 'time', 'billion','had', 'omx','us', 'russia', 'may','annual', 'day', 'both',
              'tsla','while', 'before','months', 'number', 'march', 'october', 'euros',
              'they','through', 'april']
Stopwords.update(domain_words)

def Text_Processing(Text):
    Processed_Text = list()
    Lemmatizer = WordNetLemmatizer()

    # Tokens of Words
    Tokens = nltk.word_tokenize(Text)

    for word in Tokens:
        if word not in Stopwords:
            Processed_Text.append(Lemmatizer.lemmatize(word))
    return(" ".join(Processed_Text))

tfidf = pickle.load(open("C:/Users/hp/Desktop/project sentiment analysis/tf_idf_model.pkl",'rb'))
model = pickle.load(open('C:/Users/hp/Desktop/project sentiment analysis/SVM_Tfidf_Clf.pkl','rb'))

st.title("Financial Sentiment Analysis")
text_input = st.text_area("please Enter Sentence")

if st.button('Analyze'):

    # 1. preprocess
    cleaned_text = text_cleaning(text_input)
    processed_text=Text_Processing(cleaned_text)

    # 2. vectorize
    vector_input = tfidf.transform([processed_text])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 0:
        st.markdown('Sentiment:: Negative Statement :angry: ')
    elif result == 1:
        st.markdown('Sentiment:: Neutral Statement :neutral_face: ')
    elif result == 2:
        st.markdown('Sentiment:: Positive Statement  :blush: ')

# -*- coding: utf-8 -*-
"""Final_URL_Classification_Language_NLP_Word_Embeddings_Neural_Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GAM21pS68rZSLADQei-2EQ0GkbauVbrh

# Load Libaraies
"""

import tensorflow
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import random
random.seed(123)
from tensorflow import set_random_seed
set_random_seed(123)
import time
start_time = time.time()

"""# Open Data"""

from google.colab import drive
drive.mount('/content/drive')

"""**URL Classification Dataset**"""

# URL Classification Dataset
dataframe = pd.read_csv(open('/content/drive/Shared drives/OPIM 5770 Capstone/Data/Final/df_origin.csv'), sep=',', header=0)
df_origin = pd.DataFrame(dataframe)
print(df_origin.shape)
df_origin.head()

"""We found that some duplicated URLs in the dataset and some of them are in more than one category.

To simplify the classification, we decided to keep only one category for each URL and drop the other duplicated rows.
"""

# URLs with multi categories
df_origin.sort_values('URL', inplace=True)
multi_cate = df_origin[df_origin.duplicated(subset='URL', keep=False)==True]
multi_cate

# Export URLs with multi categories later
multi_cate_export = multi_cate.iloc[:,0:-1]
multi_cate_export

# Keep only one category for each URL
df_origin.sort_values('Serial Number', inplace=True)
df_origin.drop_duplicates(subset='URL', keep='first', inplace=True)
df_origin[df_origin.duplicated(subset='URL', keep=False)==True]

# 869827 URLs left after dropping duplicated rows
print(df_origin.shape)
df_origin.head()

"""**UCI News Dataset**

We randomly selected 30000 urls from the UCI News Dataset. After excluding invalid urls, we have 19702 urls with the content.

We added 19702 urls of news to the URL Classification Dataset.

Then, all categories would have at least 10000 records.
"""

# UCI News Dataset
dataframe = pd.read_csv(open('/content/drive/Shared drives/OPIM 5770 Capstone/Data/Final/df_news_uci.csv'), sep=',', header=0)
df_news_uci = pd.DataFrame(dataframe)
print(df_news_uci.shape)
df_news_uci.head()

# Add category as 'News'
df_news_uci['Category'] = 'News'
df_news_uci = df_news_uci[['Serial Number', 'URL', 'Category', 'Clean Content']]
df_news_uci.head()

# Concat datasets
df_urls = pd.concat([df_origin, df_news_uci], ignore_index=True)
df_urls

# Totally 889529 rows and 4 columns
df_urls.shape

# 15 categories
category = df_urls['Category'].unique()
category

# Check for missing values
df_urls.isnull().sum()

"""# Analysis Data"""

# Split the dataset by category
df_urls_adult = df_urls[df_urls['Category']=='Adult']
df_urls_arts = df_urls[df_urls['Category']=='Arts']
df_urls_business = df_urls[df_urls['Category']=='Business']
df_urls_computers = df_urls[df_urls['Category']=='Computers']
df_urls_games = df_urls[df_urls['Category']=='Games']
df_urls_health = df_urls[df_urls['Category']=='Health']
df_urls_home = df_urls[df_urls['Category']=='Home']
df_urls_kids = df_urls[df_urls['Category']=='Kids']
df_urls_news = df_urls[df_urls['Category']=='News']
df_urls_recreation = df_urls[df_urls['Category']=='Recreation']
df_urls_reference = df_urls[df_urls['Category']=='Reference']
df_urls_science = df_urls[df_urls['Category']=='Science']
df_urls_shopping = df_urls[df_urls['Category']=='Shopping']
df_urls_society = df_urls[df_urls['Category']=='Society']
df_urls_sports = df_urls[df_urls['Category']=='Sports']

# Drop content with errors in adult
error_adult = df_urls_adult[df_urls_adult['Clean Content'].str.contains('error')==True].index
df_urls_adult.drop(error_adult, inplace=True)
df_urls_adult

# Analysis data
df_urls_list = [df_urls_adult, df_urls_arts, df_urls_business, df_urls_computers, df_urls_games,
                df_urls_health, df_urls_home, df_urls_kids, df_urls_news, df_urls_recreation,
                df_urls_reference, df_urls_science, df_urls_shopping, df_urls_society, df_urls_sports]
df_urls = pd.concat(df_urls_list, ignore_index=True)
df_urls.reset_index(drop=True, inplace=True)
print(df_urls.shape)
df_urls.head()

# Analysis data without adult urls (to be used in sampling)
df_urls_others_list = [df_urls_arts, df_urls_business, df_urls_computers, df_urls_games,
                       df_urls_health, df_urls_home, df_urls_kids, df_urls_news, df_urls_recreation,
                       df_urls_reference, df_urls_science, df_urls_shopping, df_urls_society, df_urls_sports]
df_urls_others = pd.concat(df_urls_others_list, ignore_index=True)
df_urls_others.reset_index(drop=True, inplace=True)
print(df_urls_others.shape)
df_urls_others.head()

# Count of data by category
category_counts = df_urls['Category'].value_counts()
category_counts = category_counts.rename_axis('Category').reset_index(name='Counts')
category_counts.sort_values('Category', inplace=True)
category_counts

# Visualize the dataset
plt.figure(figsize=(16,8))
sns.barplot(x='Category', y='Counts', data=category_counts, color='lightsteelblue')
plt.show()

"""# Sample Data

Train on a sample of 150000 (undersampled), and test on a sample of 50000 (including 3000 adult urls)
"""

# Train data: Undersampling
train_adult = df_urls_adult.sample(n=10000, random_state=123)
train_arts = df_urls_arts.sample(n=10000, random_state=123)
train_business = df_urls_business.sample(n=10000, random_state=123)
train_computers = df_urls_computers.sample(n=10000, random_state=123)
train_games = df_urls_games.sample(n=10000, random_state=123)
train_health = df_urls_health.sample(n=10000, random_state=123)
train_home = df_urls_home.sample(n=10000, random_state=123)
train_kids = df_urls_kids.sample(n=10000, random_state=123)
train_news = df_urls_news.sample(n=10000, random_state=123)
train_recreation = df_urls_recreation.sample(n=10000, random_state=123)
train_reference = df_urls_reference.sample(n=10000, random_state=123)
train_science = df_urls_science.sample(n=10000, random_state=123)
train_shopping = df_urls_shopping.sample(n=10000, random_state=123)
train_society = df_urls_society.sample(n=10000, random_state=123)
train_sports = df_urls_sports.sample(n=10000, random_state=123)
train_list = [train_adult,train_arts,train_business,train_computers,train_games,
        train_health,train_home,train_kids,train_news,train_recreation,
        train_reference,train_science,train_shopping,train_society,train_sports]
train_data = pd.concat(train_list, ignore_index=True)
train_data.reset_index(drop=True, inplace=True)
print(train_data.shape)
print(train_data.head())
print(train_data.tail())

# Category counts
train_data['Category'].value_counts()

# Test data
# Try to test on more adult urls
test_adult = df_urls_adult.sample(n=3000, random_state=789)
test_others = df_urls_others.sample(47000,random_state=789)
test_data = pd.concat([test_adult,test_others], ignore_index=True)
test_data.reset_index(drop=True, inplace=True)
print(test_data.shape)
print(test_data.head())
print(test_data.tail())

# Category counts
test_data['Category'].value_counts()

# Data for analysis
analysis_data = pd.concat([test_data,train_data], ignore_index=True)
analysis_data.reset_index(drop=True, inplace=True)
print(analysis_data.shape)
print(analysis_data.head())
print(analysis_data.tail())

"""# Language Detection"""

!pip install pycld2

# Example of detecting language
import pycld2 as cld2
isReliable, textBytesFound, details = cld2.detect(analysis_data['Clean Content'][199999])
print(details[0][0])

# Detect language
content_lang = []
for content in analysis_data['Clean Content']:
  try:
    isReliable, textBytesFound, details = cld2.detect(content)
    lang = details[0][0]
  except:
    lang = 'Unknown'
  content_lang.append(lang)
content_lang[0:10]

analysis_data['Language'] = content_lang
analysis_data.head()

# Language counts
analysis_data['Language'].value_counts()

"""# Japanese/Chinese Tokenization"""

# Japanese
analysis_japan = analysis_data[analysis_data['Language']=='Japanese']
print(analysis_japan.shape)
analysis_japan.head()

# Chinese
analysis_chinese = analysis_data[analysis_data['Language']=='Chinese']
print(analysis_chinese.shape)
analysis_chinese.head()

"""**Japanese tokenization**"""

!pip install mecab-python3

# Example of parsing Japanese
import MeCab
wakati = MeCab.Tagger("-Owakati")
split = wakati.parse(analysis_japan.iloc[0,-2]).split()
print(split)

# Japanese parsing
japanese_split = []
for content in analysis_japan['Clean Content']:
  split = wakati.parse(content).split()
  texts = ' '.join(split)
  japanese_split.append(texts)
japanese_split[0:10]

# Update Japanese word split
analysis_data.iloc[analysis_japan.index,-2] = japanese_split
print(analysis_data.iloc[analysis_japan.index].shape)
analysis_data.iloc[analysis_japan.index].head()

"""**Chinese tokenization**"""

!pip install jieba

# Example of parsing Chinese
import jieba
seg_list = jieba.cut(analysis_chinese.iloc[1,-2], cut_all=False)
split = ' '.join(seg_list)
print(split)

# Chinese parsing
chinese_split = []
for content in analysis_chinese['Clean Content']:
  split = jieba.cut(content, cut_all=False)
  texts = ' '.join(split)
  chinese_split.append(texts)
chinese_split[0:10]

# Update Chinese word split
analysis_data.iloc[analysis_chinese.index,-2] = chinese_split
print(analysis_data.iloc[analysis_chinese.index].shape)
analysis_data.iloc[analysis_chinese.index].head()

# Analysis data preview
print(analysis_data.shape)
analysis_data.head()

# Category counts
analysis_data[50000:]['Category'].value_counts()

# Category counts
analysis_data[0:50000]['Category'].value_counts()

"""# Basic Text Data Preprocessing"""

import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Word tokenization
# Remove stop words and digits
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = stopwords.words('english') + ['www','com']
analysis_token = []
for content in analysis_data['Clean Content']:
  token = word_tokenize(content)
  filtered_token = [word for word in token if not word in stop_words]
  char_token = [word for word in filtered_token if not word.isdigit()]
  analysis_token.append(char_token)
analysis_token

import nltk
nltk.download('wordnet')

# Lemmatization
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
analysis_lemm = []
for content in analysis_token:
  word_list = []
  for word in content:
    word_lemm = lem.lemmatize(word)
    word_list.append(word_lemm)
  analysis_lemm.append(word_list)
analysis_lemm

# # Stemming
# from nltk.stem import PorterStemmer
# ps = PorterStemmer()
# analysis_stem = []
# for content in analysis_lemm:
#   word_list = []
#   for word in content:
#     word_stem = ps.stem(word)
#     word_list.append(word_stem)
#   analysis_stem.append(word_list)
# analysis_stem

"""# Advanced Text Data Processing"""

# Text feature extraction by CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(input='content',binary=False,ngram_range=(1,10),analyzer='word',min_df=2,max_df=0.5,strip_accents='unicode',stop_words=stop_words)
analysis_urls_token_count = vectorizer.fit_transform(analysis_urls_token)
analysis_urls_token_count

# Text feature transformation by TfidfTransformer
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer(use_idf=True)
analysis_urls_token_tfidf = transformer.fit_transform(analysis_urls_token_count)
analysis_urls_token_tfidf

# Perform the necessary imports
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

# Create a TruncatedSVD instance: svd
svd = TruncatedSVD(n_components=3000)

# Create a KMeans instance: kmeans
kmeans = KMeans(n_clusters=6)

# Create a pipeline: pipeline
pipeline = make_pipeline(svd,kmeans)

# Import pandas
import pandas as pd

# Fit the pipeline to articles
pipeline.fit(articles)
# Calculate the cluster labels: labels
labels = pipeline.predict(articles)

# Create a DataFrame aligning labels and titles: df
df = pd.DataFrame({'label': labels, 'article': titles})

# Display df sorted by cluster label
print(df.sort_values('label'))

# Join the text
analysis_input = []
for words in analysis_token:
  content = ' '.join(words)
  analysis_input.append(content)
analysis_input

# Length of content
content_length = []
for content in analysis_input:
  length = len(content)
  content_length.append(length)
print('Max length:',np.max(content_length))
print('Average length:',np.mean(content_length))

# Percentile of length
print('10%:',np.percentile(content_length,10))
print('15%:',np.percentile(content_length,15))
print('25%:',np.percentile(content_length,25))
print('50%:',np.percentile(content_length,50))
print('75%:',np.percentile(content_length,75))
print('85%:',np.percentile(content_length,85))
print('90%:',np.percentile(content_length,90))

# Set max_length=2000
plt.figure(figsize=(16,8))
pd.Series(content_length).plot.hist(range=(0,2000), bins=20)
plt.show()

# Word embedding
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
vocab_size = 200000
encoded_input = [one_hot(content, vocab_size) for content in analysis_input]
max_length = 2000
padded_input = pad_sequences(encoded_input, maxlen=max_length, padding='post')

"""# Modeling"""

# Encode categories
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
encoder = LabelEncoder()
encoder.fit(analysis_data['Category'])
labeled_cate = encoder.transform(analysis_data['Category'])
encoded_cate = to_categorical(labeled_cate)

X_train = padded_input[50000:]
Y_train = encoded_cate[50000:]
X_test = padded_input[0:50000]
Y_test = encoded_cate[0:50000]

print(X_train.shape)
print(X_test.shape)

# Deep Learning Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
input_dim = vocab_size + 1
def build_model():
  model = Sequential()
  model.add(Embedding(input_dim, 32, input_length=max_length))
  model.add(Flatten())
  model.add(Dense(128, activation='tanh'))
  model.add(Dropout(0.2))
  model.add(Dense(15, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model
model = build_model()
print(model.summary())

from tensorflow.keras.callbacks import ModelCheckpoint
filepath = 'NN.weights.best.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', save_best_only=True, mode='max', verbose=1)
callbacks_list = [checkpoint]
history = model.fit(X_train, Y_train, epochs=5, batch_size=64, callbacks=callbacks_list, validation_data=(X_test,Y_test), verbose=1)

"""# Model Evaluation"""

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
best_model = build_model()
best_model.load_weights('/content/NN.weights.best.hdf5')
class_label = ['Adult', 'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home', 'Kids',
               'News', 'Recreation', 'Reference', 'Science', 'Shopping', 'Society', 'Sports']

# Training predictions
pred_train = best_model.predict_classes(X_train)
pred_train_prob = best_model.predict_proba(X_train)
Y_train = labeled_cate[50000:]
print('Training Accuracy:', accuracy_score(Y_train, pred_train))

# Confusion matrix: training
con_matrix = confusion_matrix(Y_train, pred_train)
con_matrix_train = pd.DataFrame(con_matrix, columns=class_label, index=class_label)
con_matrix_train

# Precision and recall: training
print(classification_report(Y_train, pred_train, target_names=class_label))

# Testing predictions
pred_test = best_model.predict_classes(X_test)
pred_test_prob = best_model.predict_proba(X_test)
Y_test = labeled_cate[0:50000]
print('Testing Accuracy:', accuracy_score(Y_test, pred_test))

# Confusion matrix: testing
con_matrix = confusion_matrix(Y_test, pred_test)
con_matrix_test = pd.DataFrame(con_matrix, columns=class_label, index=class_label)
con_matrix_test

# Precision and recall: testing
print(classification_report(Y_test, pred_test, target_names=class_label))

# Execution time
print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ((time.time() - start_time)/60))

"""# Error Analysis"""

# Category vs Predicted category
analysis_data_test = analysis_data[0:50000]
test_results = pd.DataFrame({'URL':analysis_data_test['URL'], 'Clean Content':analysis_data_test['Clean Content'], 'Language':analysis_data_test['Language'],
               'Category':analysis_data_test['Category'], 'Predicted Category':pred_test})
test_results.head()

encoded_label = range(15)
map_list = dict(zip(encoded_label,class_label))
test_results.replace({'Predicted Category':map_list}, inplace=True)
test_results.head()

# Indentify wrong predictions
results = []
for index,row in test_results.iterrows():
  category = row[-2]
  pred_category = row[-1]
  if category==pred_category:
    result = 'Right'
  else:
    result = 'Wrong'
  results.append(result)

test_results['Accuracy'] = results
test_wrong = test_results[test_results['Accuracy']=='Wrong']
test_wrong.head()

# Languages of wrong predictions
test_wrong['Language'].value_counts()

# False nagative predictions in adult urls
test_wrong_adult_fn = test_wrong[test_wrong['Category']=='Adult']
test_wrong_adult_fn

# False positive predictions in adult urls
test_wrong_adult_fp = test_wrong[test_wrong['Predicted Category']=='Adult']
test_wrong_adult_fp

# Wrong predictions in adult
test_wrong_adult = test_wrong[test_wrong['Category']=='Adult']
test_wrong_adult['Predicted Category'].value_counts()

# Wrong predictions in arts
test_wrong_arts = test_wrong[test_wrong['Category']=='Arts']
test_wrong_arts['Predicted Category'].value_counts()

# Wrong predictions in business
test_wrong_business = test_wrong[test_wrong['Category']=='Business']
test_wrong_business['Predicted Category'].value_counts()

# Wrong predictions in computers
test_wrong_computers = test_wrong[test_wrong['Category']=='Computers']
test_wrong_computers['Predicted Category'].value_counts()

# Wrong predictions in games
test_wrong_games = test_wrong[test_wrong['Category']=='Games']
test_wrong_games['Predicted Category'].value_counts()

# Wrong predictions in health
test_wrong_health = test_wrong[test_wrong['Category']=='Health']
test_wrong_health['Predicted Category'].value_counts()

# Wrong predictions in home
test_wrong_home = test_wrong[test_wrong['Category']=='Home']
test_wrong_home['Predicted Category'].value_counts()

# Wrong predictions in kids
test_wrong_kids = test_wrong[test_wrong['Category']=='Kids']
test_wrong_kids['Predicted Category'].value_counts()

# Wrong predictions in news
test_wrong_news = test_wrong[test_wrong['Category']=='News']
test_wrong_news['Predicted Category'].value_counts()

# Wrong predictions in recreation
test_wrong_recreation = test_wrong[test_wrong['Category']=='Recreation']
test_wrong_recreation['Predicted Category'].value_counts()

# Wrong predictions in reference
test_wrong_reference = test_wrong[test_wrong['Category']=='Reference']
test_wrong_reference['Predicted Category'].value_counts()

# Wrong predictions in science
test_wrong_science = test_wrong[test_wrong['Category']=='Science']
test_wrong_science['Predicted Category'].value_counts()

# Wrong predictions in shopping
test_wrong_shopping = test_wrong[test_wrong['Category']=='Shopping']
test_wrong_shopping['Predicted Category'].value_counts()

# Wrong predictions in society
test_wrong_society = test_wrong[test_wrong['Category']=='Society']
test_wrong_society['Predicted Category'].value_counts()

# Wrong predictions in sports
test_wrong_sports = test_wrong[test_wrong['Category']=='Sports']
test_wrong_sports['Predicted Category'].value_counts()

"""# Export Results"""

num_name = range(18)
col_name = ['Serial Number', 'URL', 'Category', 'Adult', 'Arts', 'Business', 'Computers', 'Games', 'Health',
            'Home', 'Kids', 'News', 'Recreation', 'Reference', 'Science', 'Shopping', 'Society', 'Sports']
rename_list = map_list = dict(zip(num_name, col_name))

# Training: Prediction prob
pred_train_prob = pd.DataFrame(pred_train_prob, columns=class_label)
df_NN_train = pd.concat([train_data.iloc[:,0:3], pred_train_prob], axis=1, ignore_index=True)
df_NN_train.rename(rename_list, axis=1, inplace=True)
df_NN_train

# Testing: Prediction prob
pred_test_prob = pd.DataFrame(pred_test_prob, columns=class_label)
df_NN_test = pd.concat([test_data.iloc[:,0:3], pred_test_prob], axis=1, ignore_index=True)
df_NN_test.rename(rename_list, axis=1, inplace=True)
df_NN_test

from google.colab import files
# URLs with multi categories
multi_cate_export.to_csv('multi_cate_export.csv', index=False)
# Prediction probability
df_NN_train.to_csv('df_NN_train.csv', index=False)
df_NN_test.to_csv('df_NN_test.csv', index=False)
# False negatives and false positives in adult
test_wrong_adult_fn.to_csv('test_wrong_adult_fn.csv', index=False)
test_wrong_adult_fp.to_csv('test_wrong_adult_fp.csv', index=False)
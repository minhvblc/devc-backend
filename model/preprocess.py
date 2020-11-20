import re
import pandas as pd
import numpy as np

import os
dirname = os.path.dirname(__file__)

from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

#process materials:
ev_path = dirname + "/processors/Englishwords.xlsx"
sf_path =  dirname + "/processors/Shortform.xlsx"
stopwords_vn_path = dirname + "/processors/stopwords_vn_dash.txt"
englishwords = pd.read_excel(ev_path, index_col= "English")
shortform = pd.read_excel(sf_path, index_col= "Short")

#phraser for word2vec
bigram = Phraser.load(dirname + "/saves/bigram.pkl")

#word2vec model:
w2vmodel = Word2Vec.load(dirname + "/saves/w2vmodel.model")
w2vdict = w2vmodel.wv

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
def preprocess(text):
  #bỏ tag html và emoji
  text = re.sub('<[^>]*>', '', text)
  text = deEmojify(text)

  #thay chữ cái viết hoa thành viết thường
  text = text.lower()

  #xóa dấu ngắt câu, xóa link và các chữ có chứa chữ số
  clean_text = []
  punc_list = '.,;:?!/\|'
  for w in (text.split()):
    if "http" in w:
      continue
    elif any(char.isdigit() for char in w):
      continue
    clean_text.append(w)
  text = ' '.join(clean_text)
  for punc in punc_list:
    text = text.replace(punc, ' ')

  #xóa bỏ các chữ cái lặp liên tiếp nhau (đỉnhhhhhhhhhh, vipppppppppppppppp)
  length = len(text)
  char = 0
  while char <length-1:
    if text[char] == text[char+1]:
      text = text[:char]+text[char+1:]
      #print(text)
      length-=1
      continue
    char+=1  
  
  #chuyển đổi các từ tiếng anh và viết tắt thông dụng sang tiếng Việt chuẩn:
  numbers = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
  text_split = text.split()
  for i, w in enumerate(text_split):
    if w in englishwords.index:
      text_split[i] = str(englishwords.loc[w, "Vietnamese"])
    if w in shortform.index:
      text_split[i] = str(shortform.loc[w, "Long"])
    if w.isdigit():
      text_split[i] = ' '.join([numbers[int(c)] for c in w]) 
  text = ' '.join(text_split)

  #loại bỏ tất cả các kí tự đặc biệt còn lại
  digits_and_characters = 'aăâbcdđeêfghijklmnoôơpqrstuưvxywzáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ0123456789 '
  text = ''.join([i for i in text if i in digits_and_characters])
  return text

def removeUnknownwords(sentence):
  new_sentence = ' '.join([w for w in sentence.split() if w in w2vdict.vocab.keys()])
  return new_sentence
def prepros(sentences):
  new_sentences = [preprocess(sentence).split() for sentence in sentences]
  new_sentences = bigram[new_sentences]
  new_sentences = [' '.join(sentence) for sentence in new_sentences]
  new_sentences = [removeUnknownwords(sentence) for sentence in new_sentences]
  return new_sentences

def sentenceToInt(sentences, feature_leng = 50, embed_dim = 200):
  sentences_split = [sentence.split() for sentence in sentences]
  smatrix = np.zeros((len(sentences_split), feature_leng, embed_dim))
  for sen_index, sentence in enumerate(sentences_split):
    zero = np.zeros(embed_dim)
    padding = max(0, feature_leng - len(sentence))
    for word_index in range(feature_leng):
      if word_index < padding:
        smatrix[sen_index, word_index, :] = zero
      else:
        smatrix[sen_index, word_index,:] = w2vdict[sentence[word_index-padding]]
  return smatrix

def process(sentences, feature_leng = 50, embed_dim = 200):
  feature_matrix = sentenceToInt(sentences, feature_leng= 50, embed_dim= 200)
  return feature_matrix

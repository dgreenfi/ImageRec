import sklearn
from pandas import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn import cluster
import csv
import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from collections import defaultdict
from string import punctuation
from heapq import nlargest


def import_clusters(fname):
    c=[]
    spamreader = csv.reader(open(fname,'r'), delimiter=',', quotechar='"')
    for row in spamreader:
            c.append(row)
    return c

def import_reviews(file):
    f=open(file,'r')
    data=f.readlines()
    reviews=[]
    for line in data:
        rec= json.loads(line)
        reviews.append(rec)
    return reviews

def review_ngrams():
    pass


def rev_by_cluster(reviews,clusters):
    rev_clust={}
    for i,c in enumerate(clusters):
        rev_clust[str(i)]=[]

    for rev in reviews:
        for i,c in enumerate(clusters):
            if rev['asin'] in c:
                rev_clust[str(i)].append(rev)

    return rev_clust

def ngrams(rev_dict,cluster):

    raw_sents=[nltk.word_tokenize(r['reviewText'].lower()) for r in rev_dict[str(cluster)]]
    tokens=[]
    for s in raw_sents:
        tokens+=s
    stop = stopwords.words('english')
    stop+=['boot','boots','.','!',',','&','#','ca','n\'t']
    tokens_nostop=[]
    for t in tokens:
        if t not in stop:
            tokens_nostop.append(t)

    bgs=nltk.bigrams(tokens_nostop)

    fdist_bi = nltk.FreqDist(bgs).most_common(20)
    fdist_uni = nltk.FreqDist(tokens_nostop).most_common(20)
    fdist = nltk.FreqDist(bgs)
    print cluster
    print fdist_uni
    print fdist_bi
    #print fdist
    #for k,v in fdist.items():
        #if v>1:
            #print k,v


## http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """
      Compute the frequency of each of word.
      Input:
       word_sent, a list of sentences already tokenized.
      Output:
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)

def main():
    clusters=import_clusters('./outputs/clusters.csv')
    reviews=import_reviews('./data/reviews_boots.json')
    rev_dict=rev_by_cluster(reviews,clusters)
    # temporary for finding a good cluster w a lot of reviews in 500 sample
    rev_count=[]
    for k in rev_dict.keys():
        rev_count.append(len(rev_dict[k]))

    #choose max index
    max_index=rev_count.index(max(rev_count))
    ngrams(rev_dict,max_index)
    ngrams(rev_dict,3)



    fs = FrequencySummarizer()
    text=' '.join([r['reviewText'].lower() for r in rev_dict[str(max_index)]])
    for s in fs.summarize(text, 5):
        print '*',s





if __name__ == '__main__':
    main()
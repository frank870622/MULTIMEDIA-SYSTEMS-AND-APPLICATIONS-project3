# -*- coding: utf-8 -*-

import numpy as np
from scipy import spatial
from gensim.models import word2vec

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words> 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def main():
    model = word2vec.Word2Vec.load("word2vec_50.model")
    index2word_set = set(model.wv.index2word)
    s1_afv = avg_feature_vector('為什麼 PTT 這麼 多人 看 棒球？', model=model, num_features=50, index2word_set=index2word_set)
    s2_afv = avg_feature_vector('肥宅 才 看 棒球 系壘 一堆 胖子', model=model, num_features=50, index2word_set=index2word_set)
    sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
    print(sim)

if __name__ == "__main__":
    main()
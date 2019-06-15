import jieba
import numpy as np
from langconv import *
from gensim.models import word2vec
from gensim.test.utils import common_texts
# 讀入字典
jieba.set_dictionary('extra_dict/dict.txt.big')
model = "wiki.word2vec_50.bin" # 載入模組
model_w2v = word2vec.Word2Vec.load(model)

# 設定 output
outputfile = open('F74056166.csv', 'w', encoding='utf-8')
# 讀入題目
with open("q500.txt", encoding='utf-8')as inputline:
    for line in inputline:
        line = line.strip('\n')                     # 去除換行符號
        line = Converter('zh-hant').convert(line)   # 讀入字串轉為正體中文
        output = line.split("\t", 1)                # 切割題題目與選項
        text = output[0]                            # 分開題目
        answer = output[1].split("\t")              # 分開每個選項
        
        # 以 jieba 切割題目，並去除 stopword
        words = list(jieba.cut(text.strip()))
        word = []   # 當前的題目儲存在這裡
        for w in words:     # 去除 stopword
            if w not in model_w2v.wv.vocab:
                print("input word %s not in dict. skip this turn" % w)
            else:
                word.append(w)

        print(word)
        
        eachans = []    #每題的四個選項儲存在這裡
        # 以 jieba 切割每個選項，並去除 stopword 之後再儲存成 list
        for everyans in answer: 
            answercut = []
            temp1 = "".join(everyans.split(')')[1])         # 去除選項的號碼部分 (1) 
            answercuts = jieba.cut(temp1, cut_all=False)    # 斷詞
            for checkvocab in answercuts:                   # 去除 stopword
                if checkvocab in model_w2v.wv.vocab:
                    answercut.append(checkvocab)
                else:
                    print("answer word %s not in dict. skip this turn" % checkvocab)
            eachans.append(list(answercut))
        
        print(eachans)


        score = []  #四個選項的分數儲存在這裡
        
        # 將四個選項與題目比較相似度
        score.append(model_w2v.n_similarity(word, eachans[0]))
        score.append(model_w2v.n_similarity(word, eachans[1]))
        score.append(model_w2v.n_similarity(word, eachans[2]))
        score.append(model_w2v.n_similarity(word, eachans[3]))
        choose = np.argmax(score) + 1
        outputfile.write('[' + str(choose) + ']\n')
            

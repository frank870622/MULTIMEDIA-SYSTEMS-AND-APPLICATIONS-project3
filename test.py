import jieba
from langconv import *
from gensim.models import word2vec
from gensim.test.utils import common_texts
word_dictionary = []

with open('gossiping.txt', 'r', encoding='utf-8') as content :
    for texts_num, line in enumerate(content):
        line = line.strip('\n')
        line = Converter('zh-hant').convert(line)
        line = line.split("\t")
        dict_page = {texts_num : line[1]}
        word_dictionary.append(dict_page)

        if (texts_num + 1) % 10000 == 0:
            print("已完成前 %d 行的store" % (texts_num + 1))

print(word_dictionary[15])

outputfile = open('F74056166.csv', 'w', encoding='utf-8')
#jieba.load_userdict("./wiki_seg.txt")
#jieba.set_dictionary("wiki_seg.txt")
jieba.set_dictionary('extra_dict/dict.txt.big')
model = "wiki.word2vec_50.bin"
model_w2v = word2vec.Word2Vec.load(model)
candidates = []
with open("wiki_seg.txt", encoding='utf-8')as f:
    for line in f:
        candidates.append(line.strip().split())

with open("oneinput.txt", encoding='utf-8')as inputline:
    for line in inputline:
        line = line.strip('\n')
        line = Converter('zh-hant').convert(line)
        output = line.split("\t", 1)
        text = output[0]
        answer = output[1].split("\t")
        eachans = []
        for everyans in answer:
            temp1 = "".join(everyans.split(')')[1])
            #print(answercut)
            eachans.append(temp1)
        
        print(text)
        print('\n')
        print(eachans)
        print('\n')
        words = list(jieba.cut(text.strip()))

        word = []
        for w in words:
            if w not in model_w2v.wv.vocab:
                print("input word %s not in dict. skip this turn" % w)
            else:
                word.append(w)

        print(word)
        flag = False
        res = []
        index = 0
        for candidate in candidates:
            for c in candidate:
                if c not in model_w2v.wv.vocab:
                    print("candidate word %s not in dict. skip this turn" % c)
                    flag = True
            if flag:
                break
            score = model_w2v.n_similarity(word, candidate)
            if score > 0.8:
                resultInfo = {'id': index, "score": score, "text": " ".join(candidate)}
                resultInfo['text'] = resultInfo['text'].replace(" ", "")
                findflag = False
                for j in range(len(eachans)):
                    if eachans[j] in word_dictionary[index]:
                        print(j+1)
                        findflag = True
                #print(resultInfo['text'])
                res.append(resultInfo)
                index += 1
                if findflag:
                    break

        res.sort(key=lambda x: x['score'], reverse=True)
        result = [] 
        for i in range(len(res)):
            if res[i]['score'] > 0.8:
                dict_temp = {res[i]['id']: res[i]['text'], 'score': res[i]['score']}
                result.append(dict_temp)


        #output = result[0]["id"].replace(" ", "")
        #print(result)


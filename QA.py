import jieba
from langconv import *
from gensim.models import word2vec
from gensim.test.utils import common_texts
# 讀入字典
jieba.set_dictionary('extra_dict/dict.txt.big')
model = "wiki.word2vec_50.bin" # 載入模組
model_w2v = word2vec.Word2Vec.load(model)

# 將斷詞語料庫儲存成list
candidates = []
with open("wiki_seg.txt", encoding='utf-8')as f:
    for line in f:
        candidates.append(line.strip().split())
# 設定output
outputfile = open('F74056166.csv', 'w', encoding='utf-8')
# 讀入題目 input.txt
with open("input.txt", encoding='utf-8')as inputline:
    for line in inputline:
        line = line.strip('\n')
        line = Converter('zh-hant').convert(line)   # 讀入字串轉為正體中文
        output = line.split("\t", 1)                # 切割題題目與選項
        text = output[0]                            # 分開題目
        answer = output[1].split("\t")              # 分開每個選項
        eachans = []
        # 以jieba切割每個選項，並去除 stopword 之後在組合回去
        for everyans in answer: 
            answercut = []
            temp1 = "".join(everyans.split(')')[1].replace(" ", "").split())
            answercuts = jieba.cut(temp1, cut_all=False)
            for checkvocab in answercuts:
                if checkvocab in model_w2v.wv.vocab:
                    answercut.append(checkvocab)
                else:
                    print("answer word %s not in dict. skip this turn" % checkvocab)
            eachans.append("".join(list(answercut)))

        # 以jieba切割題目，並去除 stopword
        words = list(jieba.cut(text.strip()))
        word = []
        for w in words:
            if w not in model_w2v.wv.vocab:
                print("input word %s not in dict. skip this turn" % w)
            else:
                word.append(w)

        print(word)
        flag = False
        findflag = False    # 用來判斷是不是找到了答案
        res = []
        index = 0
        for candidate in candidates:
            # 確認有沒有發現不在model裡的字詞
            for c in candidate:
                if c not in model_w2v.wv.vocab:
                    print("candidate word %s not in dict. skip this turn" % c)
                    flag = True
            if flag:
                break
            # 開始比對字串相似度
            score = model_w2v.n_similarity(word, candidate)
            resultInfo = {'id': index, "score": score, "text": " ".join(candidate)}
            resultInfo['text'] = resultInfo['text'].replace(" ", "")
            # 如果 score > 0.7 則確認這個字串有沒有在選項裡，如果有，輸出答案並結束比對
            if score > 0.7:
                for j in range(len(eachans)):
                    if eachans[j] in resultInfo['text']:
                        outputfile.write(str(j+1))
                        outputfile.write('\n')
                        print(j+1)
                        findflag = True
                        print(resultInfo['text'])
            # 將比對分數和字串儲存
            res.append(resultInfo)
            index += 1
            if findflag:
                break
        # 排序儲存的答案和分數
        res.sort(key=lambda x: x['score'], reverse=True)
        # 如果在 > 0.7 的結果中沒有找到答案的話，則尋找最高分的選項
        if findflag is False:
            for i in range(len(res)):
                for j in range(len(eachans)):
                    if eachans[j] in res[i]['text']:
                        outputfile.write(str(j+1))
                        outputfile.write('\n')
                        print(j+1)
                        findflag = True
                        print(res[i]['text'])
                if findflag:
                    break

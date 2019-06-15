import jieba
from langconv import *

# 載入字典
jieba.set_dictionary('extra_dict/dict.txt.big')

# 載入 stopwords
stopword_set = set()
with open('extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
    for stopword in stopwords:
        stopword_set.add(stopword.strip('\n'))

# 將斷詞好的檔案儲存成 wiki_seg.txt
output = open('wiki_seg.txt', 'w', encoding='utf-8')

# 斷詞部分
with open('gossiping.txt', 'r', encoding='utf-8') as content :
    for texts_num, line in enumerate(content):
        line = line.strip('\n')                     # 去除換行符號
        line = Converter('zh-hant').convert(line)   # 將文字轉成正體中文
        words = jieba.cut(line, cut_all=False)      # 用 jieba 斷詞
        for word in words:                          # 如果斷詞的字是 stopwords 將它去除
            if word not in stopword_set:            # 反之，將它 output
                output.write(word + ' ')
        output.write('\n')
        if (texts_num + 1) % 10000 == 0:            # 每 10000 行顯示進度
            print("已完成前 %d 行的斷詞" % (texts_num + 1))
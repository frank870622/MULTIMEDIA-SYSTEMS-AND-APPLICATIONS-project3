from gensim.models import word2vec
from gensim.test.utils import common_texts

# 載入斷詞好的PTT擋
sentences = word2vec.LineSentence('wiki_seg.txt')
# 訓練 model
model = word2vec.Word2Vec(sentences, size = 400, window = 20, workers = 4, sg = 1, min_count=0, iter=150)
# 儲存訓練好的 model
model.save('wiki.word2vec_50.bin')

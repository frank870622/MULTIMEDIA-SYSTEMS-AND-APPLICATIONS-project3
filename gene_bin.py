from gensim.models import word2vec
from gensim.test.utils import common_texts

sentences = word2vec.LineSentence('wiki_seg.txt')
model = word2vec.Word2Vec(sentences, size = 250, window = 10, workers = 10, sg = 0, min_count=1, iter=5)
model.save('wiki.word2vec_50.bin')

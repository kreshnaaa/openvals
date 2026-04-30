
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_similarity(a: str, b: str) -> float:
    vect = CountVectorizer().fit([a, b])
    vectors = vect.transform([a, b])
    return cosine_similarity(vectors)[0][1]

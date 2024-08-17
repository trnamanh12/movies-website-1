import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Tuple

def find_index( name: str, movie2idx: pd.Series) -> int:
        return movie2idx.get(name, -1) # return -1 if not found

def load_model_and_data() -> Tuple[pd.DataFrame, TfidfVectorizer, pd.Series]:
        try:
            idx_title = pd.read_csv('./data/index_tilte.csv', index_col=0)
            with open('./model_rm/tfidf.pkl', 'rb') as f:
                tfidf = pickle.load(f)
            movie2idx = pd.Series(idx_title.index, index=idx_title['title'])
            return idx_title, tfidf, movie2idx
        except Exception as e:
            print(f"Error loading model and data: {e}")
            return pd.DataFrame(), None, pd.Series()
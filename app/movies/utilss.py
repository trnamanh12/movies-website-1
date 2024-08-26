import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Tuple
from transformers import AutoTokenizer, AutoModel
import faiss
import torch
def find_index( name: str, movie2idx: pd.Series) -> int:
        return movie2idx.get(name, -1) # return -1 if not found

def load_model_and_data() -> Tuple[pd.DataFrame, TfidfVectorizer, pd.Series]:
        try:
            idx_title = pd.read_csv('./data/movies_title3.csv', index_col=0)
            with open('./model_rm/tfidf_model1.pkl', 'rb') as f:
                tfidf = pickle.load(f)
            movie2idx = pd.Series(idx_title.index, index=idx_title['title'])
            return idx_title, tfidf, movie2idx
        except Exception as e:
            print(f"Error loading model and data: {e}")
            return pd.DataFrame(), None, pd.Series()



# Load a pre-trained model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

@torch.no_grad()
def embed_text(text: str):
    model.eval()
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    embeddings = model(**inputs).last_hidden_state
    embeddings = embeddings.mean(dim=1)
    return embeddings.squeeze().numpy()

def semantic_search(query: str) -> List[str]:
    query_embedding = embed_text(query)
    try:
        index = faiss.read_index('./data/index4sSS/faiss_index.index')
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return []

    _, index_result = index.search(query_embedding.reshape(1, -1), 12)
    try:
        idx_title = pd.read_csv('./data/movies_title3.csv', index_col=0)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

    movies_name = idx_title.iloc[index_result.squeeze()]['title'].values.tolist()
    return movies_name






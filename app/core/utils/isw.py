from bs4 import BeautifulSoup
import joblib
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

from app.core.utils.stop_words import EN_STOP_WORDS
from app.config.configuration import Config


LEMMATIZER = WordNetLemmatizer()
STEMMER = PorterStemmer()


def extract_text_from_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    raw_text = soup.getText(separator=" ", strip=True).lower()
    return raw_text[:raw_text.find("[1] http")]


def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in EN_STOP_WORDS]
    return tokens


def lemmatize(tokens):
    cont = [LEMMATIZER.lemmatize(t) for t in tokens]
    return " ".join(cont)


def stem(tokens):
    cont = [STEMMER.stem(t) for t in tokens]
    return " ".join(cont)


def vectorize_dataframe(df, content_col='text_lemm'):
    tfidf_vectorizer = joblib.load(Config.ISW_VECTORIZER_PATH)
    pca = joblib.load(Config.ISW_PCA_PATH)
    tfidf_matrix = tfidf_vectorizer.transform(df[content_col])
    return pca.transform(tfidf_matrix.toarray())

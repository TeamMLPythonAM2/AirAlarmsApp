import gzip
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.config.configuration import Config

nltk.data.path.clear()
nltk.data.path.append(Config.DOWNLOAD_DIRECTORY_NLTK)


# if there is a problem with certificates uncomment next line
# import certifi
# import ssl
# ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

try:
    STOP_WORDS = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    nltk.download('punkt_tab', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    nltk.download('wordnet', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    STOP_WORDS = set(stopwords.words('english'))

LEMMATIZER = WordNetLemmatizer()
STEMMER = PorterStemmer()


def extract_text_from_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    raw_text = soup.getText(separator=" ", strip=True).lower()
    return raw_text[:raw_text.find("[1] http")]


def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in STOP_WORDS]
    return tokens


def lemmatize(tokens):
    cont = [LEMMATIZER.lemmatize(t) for t in tokens]
    return " ".join(cont)


def stem(tokens):
    cont = [STEMMER.stem(t) for t in tokens]
    return " ".join(cont)


def read_gzip_file(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return f.read()

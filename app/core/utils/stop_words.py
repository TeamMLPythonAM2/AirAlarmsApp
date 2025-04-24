import pandas as pd
import stanza
import re, os
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
    EN_STOP_WORDS = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    nltk.download('punkt_tab', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    nltk.download('wordnet', download_dir=Config.DOWNLOAD_DIRECTORY_NLTK)
    EN_STOP_WORDS = set(stopwords.words('english'))

stanza.download('uk', verbose=False, model_dir=Config.DOWNLOAD_DIRECTORY_STANZA)
stanza.download('ru', verbose=False, model_dir=Config.DOWNLOAD_DIRECTORY_STANZA)


def clean_stopwords(stopword_list):
    cleaned = []
    for word in stopword_list:
        word = re.sub(r"[^\sА-Яа-яЁёЇїІіЄєҐґ]", "", word)
        word = word.strip().lower().split()
        cleaned.extend(word)
    return cleaned

def read_uk_stopwords():
    df = pd.read_csv(
        os.path.join(Config.FILES_PATH, 'stopwords_ua.txt'),
        header=None,
        names=['stopwords']
    )
    return df.stopwords


RU_STOP_WORDS = clean_stopwords(stopwords.words('russian'))
UK_STOP_WORDS = clean_stopwords(read_uk_stopwords())

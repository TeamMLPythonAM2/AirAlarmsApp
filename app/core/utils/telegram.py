import stanza
import re
import pandas as pd
import joblib

from app.config.configuration import Config
from app.core.utils.stop_words import RU_STOP_WORDS, UK_STOP_WORDS
from app.core.scrapers.telegram.consts import CHANNEL_IDS


def read_telegram_messages_csv(path):
    df = pd.read_csv(path, encoding='utf-8')

    df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_convert('Europe/Kiev').dt.tz_localize(None)
    df['date'] = df['date'].apply(lambda x: x.replace(minute=0, second=0))
    df['lang'] = df['channel_id'].map(CHANNEL_IDS)

    return df.drop(columns=['id', 'channel_id'])


def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\sА-Яа-яЁёЇїІіЄєҐґ\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    stopwords = set(RU_STOP_WORDS + UK_STOP_WORDS)
    words = text.strip().lower().split()
    cleaned_words = [word for word in words if word.isalpha() and word not in stopwords]
    return ' '.join(cleaned_words)


def lemmatize_stanza(text, nlp):
    doc = nlp(text)
    return [word.lemma for sent in doc.sentences for word in sent.words]


def lemmatize_dataframe(df, content_col='content', lang_col='lang'):
    nlp_uk = stanza.Pipeline(
        'uk',
        processors='tokenize,mwt,pos,lemma',
        model_dir=Config.DOWNLOAD_DIRECTORY_STANZA,
        verbose=False
    )
    nlp_ru = stanza.Pipeline(
        'ru',
        processors='tokenize,pos,lemma',
        model_dir=Config.DOWNLOAD_DIRECTORY_STANZA,
        verbose=False
    )

    df['l_content'] = df.apply(
        lambda row: ' '.join(
            lemmatize_stanza(
                clean_text(row[content_col]),
                nlp_uk if row[lang_col] == 'uk' else nlp_ru
            )
        ), axis=1
    )
    return df


def vectorize_dataframe(df, content_col='l_content'):
    tfidf_vectorizer = joblib.load(Config.TELEGRAM_VECTORIZER_PATH)
    pca = joblib.load(Config.TELEGRAM_PCA_PATH)
    tfidf_matrix = tfidf_vectorizer.transform(df[content_col])
    return pca.transform(tfidf_matrix.toarray())

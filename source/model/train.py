import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

vietnamese_data_path = 'data/vietnamese/'
us_uk_data_path = 'data/english/'
vietnamese_model_path = 'model/vietnamese/'
us_uk_model_path = 'model/us_uk/'


def save_vietnamese():
    df = pd.read_csv(vietnamese_data_path + 'gender.csv')
    X_train = df['name']
    y_train = df['gender']
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train.astype('U'))
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    with open(vietnamese_model_path + 'model.pkl', 'wb') as f:
        pickle.dump(mnb, f)
        f.close()
    with open(vietnamese_model_path + 'count_vector.pkl', 'wb') as c:
        pickle.dump(vectorizer, c)
        c.close()


def save_us_uk():
    df = pd.read_csv(us_uk_data_path + 'gender.csv')
    X_train = df['name']
    y_train = df['gender']
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train.astype('U'))
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    with open(us_uk_model_path + 'model.pkl', 'wb') as f:
        pickle.dump(mnb, f)
        f.close()
    with open(us_uk_model_path + 'count_vector.pkl', 'wb') as c:
        pickle.dump(vectorizer, c)
        c.close()


save_vietnamese()
save_us_uk()

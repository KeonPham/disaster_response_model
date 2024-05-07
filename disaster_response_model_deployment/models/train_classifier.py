import sys
import nltk
nltk.download(['punkt', 'wordnet','stopwords'])
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV


def load_data(database_filepath):
    """
    Load data from a SQLite database.

    Parameters:
    database_filepath (str): The file path for the SQLite database.

    Returns:
    tuple: A tuple containing:
        - X (pandas.Series): Series containing messages.
        - Y (pandas.DataFrame): DataFrame containing categories.
        - category_names (list): List of category names.
    
    Steps:
    1. Create a SQLAlchemy Engine object with the specified database filepath.
    2. Read data from the 'DisasterResponse' table into a DataFrame.
    3. Extract the messages into X and the categories into Y.
    4. Get the category names.
    """

    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql('SELECT * FROM DisasterResponse', engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names

def tokenize(text):
    """
    Tokenize text data.

    Parameters:
    text (str): The text data to be tokenized.

    Returns:
    list: A list of cleaned and lemmatized tokens.

    Steps:
    1. Tokenize the input text into words.
    2. Filter out stopwords and non-alphabetic tokens.
    3. Lemmatize each token.
    4. Return the list of cleaned and lemmatized tokens.
    """

    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w not in stopwords.words("english") and w.isalpha()]
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model(clf = XGBClassifier()):
    """
    Build a machine learning pipeline.

    Parameters:
    clf (estimator, optional): The classifier to use in the pipeline. Defaults to XGBClassifier().

    Returns:
    sklearn.pipeline.Pipeline: A pipeline containing:
        - TfidfVectorizer for text feature extraction using the 'tokenize' function.
        - MultiOutputClassifier for multi-label classification using the specified classifier.

    Note:
    The default classifier is XGBClassifier.

    """
    model = Pipeline([
    ('tfidf', TfidfVectorizer(tokenizer=tokenize)),
    ('clf', MultiOutputClassifier(clf))
    ])
    
    return model


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Evaluate the performance of a machine learning model.

    Parameters:
    model (sklearn.pipeline.Pipeline): The trained model to be evaluated.
    X_test (pandas.Series): Series containing test messages.
    Y_test (pandas.DataFrame): DataFrame containing true labels for test messages.
    category_names (list): List of category names.

    Returns:
    None

    Steps:
    1. Make predictions on the test set.
    2. Print a classification report to evaluate the model's performance.
    """
    Y_pred = model.predict(X_test)
    print(classification_report(Y_test.values, Y_pred, target_names= category_names))


def save_model(model, model_filepath):
    with open(model_filepath, 'wb') as f:
        pickle.dump(model, f)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=123)
        
        print('Building model...')
        model = build_model(clf=XGBClassifier(learning_rate=0.5, n_estimators=100))
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
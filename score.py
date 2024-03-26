import pickle
import string
from nltk.corpus import stopwords
import nltk


from nltk.stem.porter import PorterStemmer


def preprocess_text(input_text):
    lowercase_text = input_text.lower()
    tokenized_text = nltk.word_tokenize(lowercase_text)
    cleaned_tokens = []
    stemmer = PorterStemmer()
    for token in tokenized_text:
        if token.isalnum():
            if token not in stopwords.words('english') and token not in string.punctuation:
                cleaned_tokens.append(stemmer.stem(token))
    processed_text = " ".join(cleaned_tokens)

    return processed_text


vectorizer = pickle.load(open('E:/vectorizer.pkl','rb'))



def score(text, model, threshold):
    # 1. preprocess
    preprocessed_text = preprocess_text(text)
    # 2. vectorize
    vector_input = vectorizer.transform([preprocessed_text])
    # 3. predict
    result = model.predict(vector_input)[0]
    propensity = result[1]
    prediction = (propensity > threshold)
    
    return prediction.item(), propensity

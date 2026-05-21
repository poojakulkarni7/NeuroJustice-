from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "client lying in court",
    "hiding evidence",
    "fake statement",
    "sharing confidential info",
    "privacy leak",
    "two clients conflict",
    "bias between clients",
    "misleading judge"
]

labels = [
    "honesty",
    "duty_to_court",
    "honesty",
    "confidentiality",
    "confidentiality",
    "conflict_of_interest",
    "conflict_of_interest",
    "duty_to_court"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

def predict_category(user_input):
    x = vectorizer.transform([user_input])
    return model.predict(x)[0]
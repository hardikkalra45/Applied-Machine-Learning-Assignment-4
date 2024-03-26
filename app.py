from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)


dictionary = joblib.load('trained_model.pkl')
model = dictionary["model"]
vectorizer = dictionary["vectorizer"]

def predict(text):
    # We assume the text is already in the desired format for the model
    text_features = vectorizer.transform([text]) 
    print(model)
    prediction = model.predict(text_features)
    propensity = model.predict_proba(text_features)[0][1]  # Probability of the spam class
    return {"prediction": str(prediction[0]), "propensity": float(propensity)}

@app.route('/score', methods=['POST'])
def score():
    data = request.json
    text = data.get('text', '')
    result = predict(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

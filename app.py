from flask import Flask, request, jsonify
from transformers import pipeline
from waitress import serve

app = Flask(__name__)

detection = pipeline("text-classification", model="ZachBeesley/Spam-Detector")

@app.route("/", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        try:
            data = request.json

            if "text" not in data:
                return jsonify(error="Missing 'text' field in request data"), 400

            text = data["text"]
            output = detection(text)

            label = output[0]['label'] == "Spam"
            score = output[0]['score']

            response_data = {
                "type": label,
                "score": round(score * 100)
            }

            return jsonify(response_data), 200
        except Exception as e:
            return jsonify(error=str(e)), 500

    elif request.method == "GET":
        return "This endpoint supports POST requests for scam detection. Use POST to detect language."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)

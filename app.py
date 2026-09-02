from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

PROFUNDO_URL = "https://api.profundoai.com/v1/chat/completions"


@app.route("/")
def home():
    return "AI API is working!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    text = data.get("text", "")
    system_prompt = data.get("system", "Ты полезный ассистент.")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    api_key = os.environ.get("PROFUNDO_API_KEY")

    if not api_key:
        return jsonify({"error": "PROFUNDO_API_KEY is not configured"}), 500

    response = requests.post(
        PROFUNDO_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gemini-3.1-pro",
            "messages": [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": text
    }
]
        },
        timeout=120
    )

    result = response.json()

    if response.status_code != 200:
        return jsonify(result), response.status_code

    return jsonify({
        "response": result["choices"][0]["message"]["content"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

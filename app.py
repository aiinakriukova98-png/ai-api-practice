
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

API_URL = os.environ.get("API_URL", "")
API_KEY = os.environ.get("API_KEY", "")


@app.route("/")
def home():
    return "AI API is working!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    text = data.get("text", "")
    system_prompt = data.get(
        "system",
        "Ты полезный ассистент."
    )
    model = data.get("model", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if not API_URL or not API_KEY:
        return jsonify({
            "error": "API configuration is missing"
        }), 500

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
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

        response.raise_for_status()
        result = response.json()

        return jsonify({
            "response": result["choices"][0]["message"]["content"]
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Failed to connect to AI provider"
        }), 502

    except (ValueError, KeyError, IndexError, TypeError):
        return jsonify({
            "error": "Invalid response from AI provider"
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

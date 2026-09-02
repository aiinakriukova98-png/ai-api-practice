from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

PROFUNDO_URL = "https://api.profundoai.com/v1/chat/completions"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    text = data.get("text", "")
    system_prompt = data.get("system", "Ты полезный ассистент.")
    model = data.get("model", "gemini-3.1-pro")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    api_key = os.environ.get("PROFUNDO_API_KEY")

    if not api_key:
        return jsonify({"error": "PROFUNDO_API_KEY is not configured"}), 500

    try:
        response = requests.post(
            PROFUNDO_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
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

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to connect to AI provider",
            "details": str(e)
        }), 502

        if response.status_code != 200:
        try:
            result = response.json()
        except ValueError:
            result = {
                "error": "AI provider returned a non-JSON error",
                "status_code": response.status_code
            }

        return jsonify(result), response.status_code

    result = response.json()

    return jsonify({
        "response": result["choices"][0]["message"]["content"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

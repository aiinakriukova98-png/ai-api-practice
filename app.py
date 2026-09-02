from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()

    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = text[:100] + ("..." if len(text) > 100 else "")

    return jsonify({
        "summary": summary
    })

@app.route("/")
def home():
    return "AI API is working!"

if __name__ == "__main__":
    app.run()

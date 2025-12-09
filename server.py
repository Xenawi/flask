from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def gemini_proxy():
    data = request.json

    api_key = data.get("api_key")
    prompt = data.get("prompt", "")
    image_b64 = data.get("image")

    if not api_key:
        return jsonify({"error": "API key missing"}), 400

    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_b64
                        }
                    }
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000, threaded=True)

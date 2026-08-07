import os

from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Gemini API client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("user/chatbox.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "Please enter a message."
        })

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("Gemini Error:", e)

        return jsonify({
            "reply": "Sorry, I could not process your request right now."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
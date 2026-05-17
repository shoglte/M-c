import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("SUPABASE_URL =", SUPABASE_URL)
def get_bot_config():
 
    url = f"{SUPABASE_URL}/rest/v1/bot_config?select=bot_token,chat_id"
 
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    data = r.json()

    if not data:
        raise Exception("No bot config found")

    return (
        data[0]["bot_token"],
        data[0]["chat_id"]
    )

@app.route('/send', methods=['POST'])
def send():

    try:

        name = request.form.get(
            'name',
            ''
        ).strip()

        phone = request.form.get(
            'phone',
            ''
        ).strip()

        text_message = request.form.get(
            'message',
            ''
        ).strip()

        if not name or not phone:

            return jsonify({
                "error": "Missing required fields"
            }), 400

        token, chat_id = get_bot_config()

        text = f"""
📩 New Submission

👤 Name: {name}

📞 Phone: {phone}

📝 Message:
{text_message}
"""

        telegram_url = (
            f"https://api.telegram.org/"
            f"bot{token}/sendMessage"
        )

        requests.post(
            telegram_url,
            data={
                "chat_id": chat_id,
                "text": text
            },
            timeout=15
        )

        image = request.files.get("image")

        if image:

            photo_url = (
                f"https://api.telegram.org/"
                f"bot{token}/sendPhoto"
            )

            requests.post(
                photo_url,
                data={
                    "chat_id": chat_id
                },
                files={
                    "photo": image
                },
                timeout=30
            )

        return jsonify({
            "success": True
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route('/')
def home():

    return "Backend Running 🫡"

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=int(
            os.getenv(
                'PORT',
                5000
            )
        )
    ) 

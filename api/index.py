from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

@app.route("/integration.json", methods=['GET'])
def integration_json():
    base_url = request.url_root.rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-21",
                "updated_at": "2025-02-21"
            },
            "descriptions": {
                "app_name": "Subscription Expiration Notifier",
                "app_description": "Notifies users when their subscription is close to expiration.",
                "app_logo": "https://hng-telex-stage3.vercel.app/logo.png",
                "app_url": base_url,
                "background_color": "#FFFFFF"
            },
            "is_active": True,
            "integration_type": "output",
            "integration_category": "Monitoring & Logging",
            "output": [
                {
                    "label": "app_channel",
                    "value": True
                }
            ],
            "key_features": [
                "Notify users before subscription expires",
                "Supports OAuth authentication",
                "Customizable reminder intervals",
                "Detailed logging of notifications"
            ],
            "permissions": {
            "monitoring_user": {
                "always_online": True,
                "display_name": "Subscription Monitor"
            }
            },
            "author": "Mariam Smith",
            "settings": [
                {
                    "label": "output",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                }
            ],
            "target_url": "https://hng-telex-stage3.vercel.app/target_url",
            "auth_initiate_url": "https://hng-telex-stage3.vercel.app/oauth/initiate",
            "is_oauthfield": True
        }
    }

@app.route('/target_url', methods=['POST'])
def target_point():
    """
    Receives data from Telex channel, schedules backgroung processess
    and immediately returns a 202 Accepted status
    """
    data = request.get_json()
    return make_response("", 202)

@app.route('/status', methods=['GET'])
def status():
    """
    Public endponit to check status of the integration
    """
    return jsonify({"message": "Subscription Expiration Notifier is running"})

if __name__ == "__main__":
    app.run
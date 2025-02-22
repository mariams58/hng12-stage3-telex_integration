from flask import Flask, request
from flask_cors import CORS
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
                "app_logo": "https://example.com/logo.png",
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
            "target_url": "https://example.com/api/notify",
            "auth_initiate_url": "https://example.com/oauth/initiate",
            "is_oauthfield": True
        }
    }

if __name__ == "__main__":
    app.run
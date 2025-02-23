from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import requests, os, time, threading
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

# Base webhook URL for notifications (fixed as specified)
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
target_url = os.getenv("target_url")
# Read the webhook slug from the environment variables
WEBHOOK_SLUG = os.getenv("WEBHOOK_SLUG")

def notify_daily(subscription: str, expiry_date: datetime.date, webhook_slug: str):
    """
    Sends a daily notification from 7 days before the subscription expires until expiration.
    Each notification is sent to channel
    with a payload in the expected JSON format.
    """
    now = datetime.now().date()
    # Determine the start date for notifications (7 days before expiry)
    start_date = expiry_date - timedelta(days=7)
    if now > start_date:
        start_date = now

    # Total number of notifications (including the expiration day)
    days_to_notify = (expiry_date - start_date).days + 1

    for i in range(days_to_notify):
        url = f"{BASE_WEBHOOK_URL}/{webhook_slug}"
        payload = {
            "event_name": "subscription_expiry_notification",
            "message": f"Your subscription for {subscription} expires on {expiry_date.strftime('%d/%m/%Y')}. Notification #{i+1}",
            "status": "success"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Notification {i+1} sent with status: {response.status_code}")
        except Exception as e:
            print(f"Error sending notification: {e}")
        # Wait 24 hours before sending the next notification
        time.sleep(86400)

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
                "app_logo": "https://imgur.com/g8KHynf",
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
                "Processes data in the background",
                "Returns 202 Accepted quickly"
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
                    "label": "subscription_slug",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                },
                {
                    "label": "Subscriptions",
                    "type": "dropdown",
                    "required": True,
                    "default": "Netflix",
                    "options": ["Netflix", "AWS", "Azure", "GCP"]
                },
                {
                    "label": "expiry_date",
                    "type": "text",
                    "required": "true",
                    "default": "dd/mm/yy"
                },
            ],
            "target_url": target_url,
        }
    }

@app.route('/target_url', methods=['POST'])
def target_point():
    """
    Receives data from Telex channel, schedules backgroung processess
    and immediately returns a 202 Accepted status
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No JSON payload provided"}), 400)
    
    settings = data.get("settings")
    webhook_slug = data.get("subscription_slug", "* * * * *")
    
    if not settings:
        return make_response(jsonify({"error": "No settings provided"}), 400)
    
    subscription_type = settings.get("Subscriptions", "Netflix")
    expiry_date_str = settings.get("expiry_date")
    
    if not expiry_date_str:
        return make_response(jsonify({"error": "expiry_date is required"}), 400)
    
    # Parse expiry_date from dd/mm/yy format
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%d/%m/%y").date()
    except Exception as e:
        return make_response(jsonify({
            "error": f"Invalid expiry_date format. Expected dd/mm/yy. {str(e)}"
        }), 400)
    
    # Launch background thread to handle daily notifications
    thread = threading.Thread(target=notify_daily, args=(subscription_type, expiry_date, webhook_slug))
    thread.start()
    return make_response("", 202)

@app.route('/status', methods=['GET'])
def status():
    """
    Public endponit to check status of the integration
    """
    return jsonify({"message": "Subscription Expiration Notifier is running"})

if __name__ == "__main__":
    app.run
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import requests, os, time, threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

# Base webhook URL for notifications (fixed as specified)
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
target_url = os.getenv("target_url")
smtp_host = os.getenv("smtp_host")
smtp_username = os.getenv("smtp_username")
smtp_password = os.getenv("smtp_password")
smtp_port = 587
# Read the webhook slug from the environment variables
WEBHOOK_SLUG = os.getenv("WEBHOOK_SLUG")

def notify_daily(subscription: str, expiry_date: datetime.date, email: str, message: str):
    """
    Sends notification of subscription expires expiration.
    Each notification is sent to email provided in the settings
    """
    days = expiry_date.days
    # Create the email message
    email_content = (
        f"Hello,\n\nYour subscription for {subscription} expires in {days+1}.\n"
        f"Additional details: {message}\n\nPlease take the necessary actions to renew."
    )
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = "Subscription Expiration Notice"
    msg.attach(MIMEText(email_content, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        logging.info(f"Email sent successfully to {email}")
    except Exception as e:
        logging.error(f"Failed to send email to {email}: {e}")


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
                "app_logo": "https://i.imgur.com/g8KHynf.png",
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
                    "label": "email",
                    "type": "text",
                    "required": True,
                    "default": ""
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
    
    settings = data.get("settings", [])
    message = data.get('message')
    
    # Extract the 'email' setting from the settings list
    email_setting = next((s for s in settings if s.get('label') == 'email'), None)
    email = email_setting.get('default') if email_setting else None
    if not email:
        return make_response(jsonify({'error': 'email setting is required'}), 400)

    subscription_setting = next((s for s in settings if s.get('label') == 'Subscriptions'), None)
    expiry_setting = next((s for s in settings if s.get('label') == 'expiry_date'), None)
    subscription = subscription_setting.get('default') if subscription_setting else "Unknown"
    expiry_date = expiry_setting.get('default') if expiry_setting else "Unknown"
    
    if not expiry_date:
        return make_response(jsonify({"error": "expiry_date is required"}), 400)
    
    # Parse expiry_date from dd/mm/yy format
    try:
        expiry_date = datetime.strptime(expiry_date, "%d/%m/%y").date()
    except Exception as e:
        return make_response(jsonify({
            "error": f"Invalid expiry_date format. Expected dd/mm/yy. {str(e)}"
        }), 400)
    
    # Launch background thread to handle daily notifications
    #thread = threading.Thread(target=notify_daily, args=(subscription, expiry_date, email))
    #thread.start()
    response = make_response("", 202)
    response.call_on_close(lambda: notify_daily(subscription, expiry_date, email, message))
    return response


@app.route('/', methods=['GET'])
def status():
    """
    Public endponit to check status of the integration
    """
    return jsonify({"message": "Subscription Expiration Notifier is running"})

if __name__ == "__main__":
    app.run
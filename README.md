# Subscription Expiration Notifier Integration

This repository contains a Flask-based output integration that monitors subscription expiration data and sends daily notifications via a webhook. The integration serves a JSON spec at `/integration.json` for configuration by the App, and it accepts incoming POST requests at `/target_url` with subscription settings. Notifications are sent daily from 7 days before the subscription expires until the expiration day.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Usage](#usage)
- [License](#license)

## Features

- **Output Integration:** Acts as a router that immediately returns a 202 Accepted status when data is received and processes notifications in the background.
- **Daily Notifications:** Sends notifications every day from 7 days before the subscription's expiry date until the subscription expires.
- **Webhook Integration:** Forwards notifications to a specified webhook URL, using a webhook slug retrieved from environment variables.
- **JSON Spec Endpoint:** Provides an integration spec at `/integration.json` for easy configuration.
- **CORS Enabled:** Supports cross-origin requests.
- **Unit Testing:** Includes tests written with pytest to verify endpoint functionality.

## Prerequisites

- Python 3.8 or later
- [pip](https://pip.pypa.io/)
- [virtualenv](https://virtualenv.pypa.io/)

## Setup

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mariams58/hng12-stage3-telex_integration
   cd hng12-stage3-telex_integration

2. **Create and activate a virtual environment:**
    - **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    - **On Windows:**
    ```bash
    python3 -m venv venv
    .venv/Scripts/activate
    ```
3. **Install the dependencies:**
```bash
    pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file in the project root directory with the following content (update the values as needed):
```
    # Unique webhook slug for your integration
    WEBHOOK_SLUG=your_unique_webhook_slug
    BASE_WEBHOOK_URL=your_unique_base_webhook_url
    target_url=your_unique_base_webhook_url/target_url
```

## Endpoint

## Testing

## Deployment

## Usage
1. Install the integration using its JSON URL at:[Integration.json](https://hng-telex-stage3.vercel.app/integration.json)

2. Set the Subscription Expiration Notifier in the settings (Org dashboard > Apps > "Subscription Expiration Notifier" > Settings), obtained from [the interation hosted url](https://hng-telex-stage3.vercel.app)

3. Ensure the integration is activated at the organisation and the individual channels you want to use it

## License
    This project is licensed under the MIT License

## Contributions
For any issues or contributions, please open an issue or submit a pull request on GitHub.
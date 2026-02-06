# Heart Attack Prediction & Alert System


A real-time medical alert system that detects abnormal heart activity and sends instant notifications via WhatsApp and automated voice calls to alert users and emergency contacts.

## Features

- **Real-time Heart Monitoring**: Detects abnormal heart activity and potential cardiac events
- **WhatsApp Alerts**: Sends instant notifications via WhatsApp with medical details
- **Automated Voice Calls**: Makes automated phone calls to notify emergency contacts
- **Secure Report Delivery**: Sends medical reports via secure token-based PDF links
- **User Subscription Management**: Users can opt-in/opt-out of alerts via WhatsApp commands
- **Medical Data**: Includes patient information, condition severity, and location details

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Communications**: Twilio (WhatsApp & Phone API)
- **Environment**: Python Virtual Environment
- **Notifications**: WhatsApp + Voice Calls

## Prerequisites

- Python 3.7+
- Twilio Account (for WhatsApp and voice calls)
- Ngrok (for local testing with webhooks)

## Installation

1. **Clone or navigate to the project directory**
    ```bash
    cd alsys
    ```

2. **Create and activate virtual environment** (already created)
    ```bash
    # On Windows
    .\Scripts\activate
    
    # On macOS/Linux
    source bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `details.env` file in the project root with the following variables:

```env
# Twilio Credentials
account_sid=your_twilio_account_sid
auth_token=your_twilio_auth_token

# WhatsApp Configuration
from_number_whatsapp=whatsapp:+1234567890 [Twilio Sandbox Whatsapp Number]


# Voice Call Configuration
from_number=+1234567890 [Twilio active number]
to_number=+1234567890 [Your Registered Mobile Number]

# Ngrok URL (for webhook testing)
NGROK_URL=https://your-ngrok-url.ngrok.io

# Report File Path
PDF_PATH=report.pdf
```

## Usage

### Starting the Server

```bash
python app.py
```

The Flask app will start on `http://localhost:5000`

### WhatsApp Commands

Users can control alerts by sending WhatsApp messages to the sandbox:

- **`start`** - Begin receiving medical alerts
- **`cancel`** - Stop receiving alerts
- **`help`** - Display help message
- **`stop`** - Leave the WhatsApp sandbox

### API Endpoints

#### POST `/whatsapp`
WhatsApp webhook endpoint that handles incoming messages and user commands.

#### GET `/pdf`
Serves the medical report PDF with a secure token.

**Parameters:**
- `token` - Secure single-use token (expires in 5 minutes)

**Example:**
```
GET /pdf?token=<secure_token>
```

#### GET `/`
Triggers the medical alert notification workflow. Sends WhatsApp message with secure PDF link and makes an automated voice call to emergency contacts.

**Response:**
```json
{
  "status": "sent",
  "message_sid": "SM1234567890abcdef"
}
```

## Alert Information Included

When an alert is triggered, the following information is sent:

- **Patient Name**: Identified patient information
- **Medical Condition**: "Heart Attack Detected" or relevant cardiac condition
- **Severity Level**: Urgency classification (e.g., "Very High")
- **Location**: Last known patient location
- **Medical Report**: PDF attachment with detailed diagnostic data

## Security Features

- **Token-Based PDF Access**: One-time use tokens that expire after 5 minutes
- **Secure WhatsApp Webhook**: Validates incoming messages
- **Environment Variables**: Sensitive credentials stored in `.env` file
- **Ngrok Tunneling**: Secure local development with ngrok

## Token Expiry

- Token expiry time: **5 minutes (300 seconds)**
- Each token can only be used **once**
- After token expires or is used, a new token must be generated

## Twilio Integration

The system uses Twilio's:
- **WhatsApp API** for text notifications
- **Voice API** for automated calls with TwiML

## Development Notes

- Uses `secrets.token_urlsafe()` for cryptographically secure tokens
- In-memory token store suitable for local testing
- Flask debug mode enabled for development

## Deployment Considerations

For production deployment:
- Switch from in-memory token storage to a database (e.g., Redis, PostgreSQL)
- Implement proper authentication and authorization
- Use HTTPS for all endpoints
- Add rate limiting for API endpoints
- Implement comprehensive error handling and logging
- Use environment-specific configurations

## File Structure

```
alsys/
├── app.py              # Main Flask application
├── details.env         # Configuration (use .env for secrets)
├── report.pdf          # Medical report template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── pyvenv.cfg          # Virtual environment config
└── [Virtual Environment Files]
```

## Troubleshooting

**WhatsApp Sandbox Issues:**
- WhatsApp Sandbox is active for 3 days only
- Users must send a message first to the sandbox to receive alerts
- Re-send "join <your sandbox code>" command after 3 days

**PDF Link Not Working:**
- Ensure Ngrok URL is correct in `details.env`
- Check token expiry (5 minutes)
- Verify the PDF file exists at the specified path

**Voice Call Not Playing:**
- Validate TwiML format
- Check phone number format matches Twilio requirements
- Ensure proper API credentials

## 🤝 Contributing

Contributions are welcome!

## Disclaimer

This system is for alerting purposes only and should not replace professional medical diagnosis or emergency services. Always call emergency services (911) for medical emergencies.

<div align="center">

**Built with ❤️**

[⬆ back to top](#heart-attack-prediction--alert-system)

</div>
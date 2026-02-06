from flask import Flask, send_file, request, abort
from twilio.rest import Client
import secrets
import time
import os
from dotenv import load_dotenv
load_dotenv('details.env')
NGROK_URL =  os.getenv("NGROK_URL")
account_sid= os.getenv("account_sid")
auth_token=os.getenv("auth_token")
client = Client(account_sid, auth_token)


PDF_PATH = os.getenv("PDF_PATH", "report.pdf")
TOKEN_EXPIRY_SECONDS = 300  # 5 minutes

# ----------------------------------------
joined_user = set(); #os.getenv("to_number")  # Replace with your WhatsApp number for testing
app = Flask(__name__)

# In-memory token store (OK for local testing)
TOKENS = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")  
    body = request.form.get("Body")
    body = body.strip().lower()
    if body == "start":
       joined_user.add(from_number)
    if body == "cancel":
        joined_user.discard(from_number)
        message = client.messages.create(
            from_= "whatsapp:"+ from_number,  
            to = "whatsapp:"+os.getenv("from_number_whatsapp"),
            body="stop"
        )
    if body == "help":
        # You can customize the help message as needed
        help_message = "Welcome to the Medical Alert System! Send 'start' to receive alerts, 'cancel' to stop receiving alerts, 'stop' to leave the sandbox any time and 'help' for this message."
        client.messages.create(
            from_="whatsapp:"+os.getenv("from_number_whatsapp"),
            to=from_number,
            body=help_message
        )
    return "", 200

@app.route("/pdf")
def serve_pdf():
    token = request.args.get("token")

    if not token or token not in TOKENS:
        abort(403)

    if TOKENS[token] < time.time():
        del TOKENS[token]
        abort(403)

    # one-time use
    del TOKENS[token]

    return send_file(
        PDF_PATH,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="report.pdf"
    )


@app.route("/")
# WhatsApp Sandbox is used for testing which is active for only 3 days
def send_notification():
    if not joined_user:
        return {
            "error": "No active WhatsApp users yet. Send any message to the sandbox first."
        }, 400

    # Use latest joined user
    to_whatsapp = list(joined_user)[-1]
    token = secrets.token_urlsafe(32)
    TOKENS[token] = time.time() + TOKEN_EXPIRY_SECONDS
    name = "John Doe"
    msg=f"Medical Alert: Abnormal heart activity detected. Please find the detailed report attached. Patient Name: {name}."
    pdf_url = f"{NGROK_URL}/pdf?token={token}"
    from_= "whatsapp:"+os.getenv("from_number_whatsapp")
    to=to_whatsapp
    message = client.messages.create(
    from_=from_,
    to=to,
    body=msg,
    media_url=[pdf_url]
)
    name = "John Doe"
    condition = "Heart Attack Detected"
    severity = "Very High"
    location = "123 Main St, Anytown, USA"
    twiml = f"""
    <Response>
        <Say voice="alice">
            This is an automated medical alert. Abnormal heart activity has been detected. The patient may be experiencing a cardiac emergency. 
            Name: {name}.
            Condition: {condition}.
            Severity: {severity}.
            Location: {location}.
            <break time="0.5s"/>
            Please seek immediate medical assistance.
        </Say>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=os.getenv("to_number"),
        from_=os.getenv("from_number"),
    )


    return {
        "status": "sent",
        "message_sid": message.sid
    }


if __name__ == "__main__":
    app.run(port=5000, debug=True)
from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio credentials (use environment variables in production)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

TWILIO_WHATSAPP_FROM =  os.getenv('TWILIO_WHATSAPP_FROM') 
YOUR_WHATSAPP_TO =  os.getenv('YOUR_WHATSAPP_TO')      

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hardware')
def hardware():
    return render_template('hardware.html')

@app.route('/coming_soon')
def coming_soon():
    return render_template('soon.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')



# @app.route('/contact', methods=['POST'])
# def handle_contact_form():
#     data = request.form

#     name = data.get('name')
#     email = data.get('email')
#     phone = data.get('phone')
#     country = data.get('country')
#     message = data.get('message')

#     # Format WhatsApp message
#     msg = f"📩 *New Contact Form Submission (SiAi)*\n\n" \
#           f"👤 Name: {name}\n📧 Email: {email}\n📱 Phone: {phone}\n" \
#           f"🌍 Country: {country}\n📝 Message: {message}"

#     # Send WhatsApp message via Twilio
#     try:
#         client.messages.create(
#             body=msg,
#             from_=TWILIO_WHATSAPP_FROM,
#             to=YOUR_WHATSAPP_TO
#         )
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        country = data.get('country')
        message = data.get('message')

        print(f"Received contact form submission: Name={name}, Email={email}, Phone={phone}, Country={country}, Message={message}")

        msg = f"📩 *New Contact Form Submission (SiAi)*\n\n" \
              f"👤 Name: {name}\n📧 Email: {email}\n📱 Phone: {phone}\n" \
              f"🌍 Country: {country}\n📝 Message: {message}"

        try:
            sent_message = client.messages.create(
                body=msg,
                from_=TWILIO_WHATSAPP_FROM,
                to=YOUR_WHATSAPP_TO
            )
            print(f"✅ WhatsApp message sent: SID={sent_message.sid}")
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            print(f"❌ Error sending WhatsApp message: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    # GET request — show contact form
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
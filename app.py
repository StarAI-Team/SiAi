from flask import Flask, render_template, request, jsonify, url_for, redirect
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)


EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "staraiinternational@gmail.com"
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  

TO_EMAIL = "staraiinternational@gmail.com"  


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hardware')
def hardware():
    return render_template('hardware.html')

@app.route('/coming_soon')
def coming_soon():
    return render_template('soon.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        country = data.get('country')
        message = data.get('message')

        body = f"""New Contact Form Submission (SiAi)

Name: {name}
Email: {email}
Phone: {phone}
Country: {country}
Message: {message}
"""

        msg = MIMEText(body)
        msg['Subject'] = '📩 New SiAi Contact Submission'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL

        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
            return redirect(url_for('contact', success=1))

        except Exception as e:
            print(f"Email error: {e}")
            return render_template('contact.html', success=0, error=str(e))

     # Render form page (check for ?success=1)
    success = request.args.get('success')
    return render_template('contact.html', success=success)



#ROUTE FOR SENDING WHATSAPP
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         data = request.form

#         name = data.get('name')
#         email = data.get('email')
#         phone = data.get('phone')
#         country = data.get('country')
#         message = data.get('message')

#         print(f"Received contact form submission: Name={name}, Email={email}, Phone={phone}, Country={country}, Message={message}")

#         msg = f"📩 *New Contact Form Submission (SiAi)*\n\n" \
#               f"👤 Name: {name}\n📧 Email: {email}\n📱 Phone: {phone}\n" \
#               f"🌍 Country: {country}\n📝 Message: {message}"

#         try:
#             sent_message = client.messages.create(
#                 body=msg,
#                 from_=TWILIO_WHATSAPP_FROM,
#                 to=YOUR_WHATSAPP_TO
#             )
#             print(f"✅ WhatsApp message sent: SID={sent_message.sid}")
#             return jsonify({'status': 'success'}), 200
#         except Exception as e:
#             print(f"❌ Error sending WhatsApp message: {e}")
#             return jsonify({'status': 'error', 'message': str(e)}), 500

#     # GET request — show contact form
#     return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)



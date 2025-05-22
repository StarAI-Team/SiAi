from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
import smtplib
from email.mime.text import MIMEText
import os
from flask_compress import Compress
from flask_minify import minify

app = Flask(__name__)
app.secret_key = 'su467pe52rsec58654532ret452k562ey'
minify(app=app, html=True, js=True, cssless=True, bypass=['image/', 'video/', 'application/octet-stream'])

Compress(app)

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
                
            flash("✅ Thank you! Your message has been sent.", "success")
        except Exception as e:
            print(f"Email error: {e}")
            flash("❌ There was an error sending your message. Please try again.", "error")

        return redirect(url_for('contact'))

    return render_template('contact.html')

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
@app.after_request
def final_after_request_handler(response):
    # 🔁 Add cache headers for static files
    if 'Cache-Control' not in response.headers and request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'

    # 🚫 Skip minify on binary content
    content_type = response.headers.get('Content-Type', '')
    if any(binary in content_type for binary in ['image/', 'video/', 'audio/', 'application/octet-stream']):
        response.direct_passthrough = True

    return response


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



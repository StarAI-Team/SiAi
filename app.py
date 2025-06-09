from flask import Flask, render_template, request, url_for, flash, redirect, session
import smtplib
from email.mime.text import MIMEText
import os
from flask_compress import Compress
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFError


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
#app.secret_key = '426yvbdwi'

limiter = Limiter(app=app, key_func=get_remote_address)
Compress(app)
csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    app.logger.error(f"CSRF error: {e.description}")
    flash("⚠️ CSRF token missing or invalid. Please refresh the page and try again.", "error")
    return redirect(url_for('contact'))


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  


# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# EMAIL_ADDRESS = "staraiinternational@gmail.com"
# EMAIL_PASSWORD = 'ppis pfap upqq bfea'


TO_EMAIL = "staraiinternational@gmail.com"  

# @app.route('/static/<path:filename>')
# def static_files(filename):
#     response = make_response(send_from_directory('static', filename))
#     # Cache for 30 days (2592000 seconds) and mark as immutable
#     response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
#     return response

csp = {
    'default-src': [
        '\'self\'',
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',         
        'https://cdnjs.cloudflare.com',    
        '\'unsafe-inline\'',                
        'https://fonts.googleapis.com'    
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',         
        'https://cdnjs.cloudflare.com',    
        '\'unsafe-inline\'',                
        '\'unsafe-eval\''                   
    ],
    'font-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com',    
        'https://fonts.gstatic.com'        
    ],
    'img-src': [
        '\'self\'',
        'data:',                           
    ],
    'connect-src': [
        '\'self\'',
    ],
}
Talisman(app, content_security_policy=csp)


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
@limiter.limit("5 per hour")
def contact():
    if request.method == 'POST':
        print(f"Session keys: {list(session.keys())}")
        print(f"CSRF token in session: {session.get('csrf_token')}")
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


@app.after_request
def add_cache_headers(response):
    if 'Cache-Control' not in response.headers and request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response



if __name__ == '__main__':
    app.run(debug=True, port=8000)



# @app.route('/static/<path:filename>')
# def static_files(filename):
#     response = make_response(send_from_directory('static', filename))
#     # Cache for 30 days (2592000 seconds) and mark as immutable
#     response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
#     return response

# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     app.logger.error(f"CSRF error: {e.description}")
#     flash("⚠️ CSRF token missing or invalid. Please refresh the page and try again.", "error")
#     return redirect(url_for('contact'))

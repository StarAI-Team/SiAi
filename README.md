# SiAi Hardware Website

This project is a web application for showcasing AI hardware and computing devices for schools, startups, and farmers across Africa. It is built using Python (likely Flask), HTML, CSS (Tailwind, custom styles), and JavaScript (Swiper.js, AOS.js).

## Project Structure

```
app.py                # Main application file (Flask or similar)
extras.py             # Additional Python logic
static/               # Static assets (images, videos, styles)
  images/hardware/    # Hardware device images
  styles/siai.css     # Custom CSS
  ...
templates/            # HTML templates (Jinja2/Flask)
  hardware.html       # Main hardware showcase page
  ...
Pipfile, Pipfile.lock # Python dependencies
Procfile              # For deployment (e.g., Heroku)
robots.txt            # SEO robots file
siai-website-plan.docx# Project planning document
```

## Getting Started

### 1. Install Python Dependencies

This project uses Pipenv for dependency management. Install Pipenv if you don't have it:

```bash
pip install pipenv
```

Install dependencies:

```bash
pipenv install
```

### 2. Run the Application

Activate the virtual environment and start the app:

```bash
pipenv shell
python app.py
```

The app should be available at `http://localhost:5000` (or as configured in `app.py`).

### 3. Static Assets
- All images, videos, and styles are in the `static/` folder.
- Update hardware images in `static/images/hardware/`.
- Custom styles are in `static/styles/siai.css`.

### 4. Templates
- Main page: `templates/hardware.html`
- Other pages: `templates/index.html`, `contact.html`, etc.
- Use Jinja2 templating for dynamic content if using Flask.

### 5. Deployment
- The `Procfile` is set up for platforms like Heroku.
- Ensure all environment variables required by `app.py` are set.

### 6. Frontend Libraries
- [Tailwind CSS](https://tailwindcss.com/) for utility-first styling.
- [Swiper.js](https://swiperjs.com/) for carousels.
- [AOS.js](https://michalsnik.github.io/aos/) for scroll animations.
- [Font Awesome](https://fontawesome.com/) for icons.

### 7. SEO & Metadata
- `robots.txt` and meta tags in HTML for SEO.
- Update `sitemap.xml` in `static/` as needed.

## Contributing
- Follow Python and HTML best practices.
- Keep static assets organized.
- Document any new features or changes in this README.

## Troubleshooting
- If static files do not load, check Flask static folder configuration.
- For deployment issues, verify the `Procfile` and required environment variables.

## Contact
For questions, reach out to the project owner or check the planning document `siai-website-plan.docx`.

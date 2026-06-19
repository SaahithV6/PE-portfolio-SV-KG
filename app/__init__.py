import os
from flask import Flask, render_template
from dotenv import load_dotenv
from .data import EXPERIENCES, EDUCATION, HOBBIES, LOCATIONS

load_dotenv()
app = Flask(__name__)

NAV_PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
]


@app.context_processor
def inject_nav_pages():
    return dict(nav_pages=NAV_PAGES)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        experiences=EXPERIENCES,
        education=EDUCATION,
    )
    
@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", hobbies=HOBBIES)

import os
from flask import Flask, render_template
from dotenv import load_dotenv
from .data import EXPERIENCES, EDUCATION, HOBBIES, LOCATIONS

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        experiences=EXPERIENCES,
        education=EDUCATION,
    )

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# Vercel handler
from vercel_wsgi import handle

def handler(event, context):
    return handle(app, event, context)

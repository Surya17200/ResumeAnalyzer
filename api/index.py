from app import app
from vercel_wsgi import handler

# This is the function Vercel calls
def handler(event, context):
    return handler(app, event, context)

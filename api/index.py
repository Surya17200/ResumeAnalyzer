from app import app
import vercel_wsgi

# Correct handler for Vercel
def handler(event, context):
    return vercel_wsgi.handle(app, event, context)

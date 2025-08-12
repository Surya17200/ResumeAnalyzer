from app import app
import vercel_wsgi

# Expose the handler Vercel will call
handler = lambda event, context: vercel_wsgi.handle(app, event, context)

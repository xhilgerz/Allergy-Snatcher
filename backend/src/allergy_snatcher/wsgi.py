from a2wsgi import ASGIMiddleware
from allergy_snatcher.__main__ import main

# main() returns the raw WSGI app
wsgi_app = main()

# Wrap the WSGI app to make it ASGI-compatible for Uvicorn
app = ASGIMiddleware(wsgi_app)

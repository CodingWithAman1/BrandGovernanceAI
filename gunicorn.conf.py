import os

# Render dynamically assigns the port via the PORT environment variable
port = os.environ.get('PORT', '5000')

# Bind to 0.0.0.0 so Render can detect and route external traffic
bind = f"0.0.0.0:{port}"

# Worker and concurrency settings for production stability
workers = int(os.environ.get('WEB_CONCURRENCY', '2'))
threads = int(os.environ.get('PYTHON_MAX_THREADS', '2'))
timeout = 120

# Stream logs to stdout/stderr for Render log stream
accesslog = '-'
errorlog = '-'
loglevel = 'info'

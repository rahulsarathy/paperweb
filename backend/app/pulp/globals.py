import os

# NGROK
NGROK_HOST='95c0c850.ngrok.io'

# GOOGLE
GOOGLE_MAPS_PLACES = 'AIzaSyAStU9SHXwqw6iyBonOjkIQtzgQ8FguR3U'

# STRIPE
STRIPE_API_KEY = 'sk_test_gZ50gEoA6E8vcDZC3IZVyVqi00e5FInywM'
STRIPE_PUBLIC_KEY = 'pk_test_9DUWDnI9T5YJWmLRhNn6nHtS'
PULP_STRIPE_PLAN = 'plan_GAWq4OuTaB2RqS'

# AWS S3
S3_USER_ACCESS_ID = os.environ.get('AWS_ACCESS_KEY_ID')
S3_USER_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
PDF_BUCKET = os.environ.get('AWS_PDF_BUCKET')
HTML_BUCKET = os.environ.get('AWS_HTML_BUCKET')

# POCKET
POCKET_CONSUMER_KEY = os.environ.get('POCKET_CONSUMER_KEY')

# INSTAPAPER
INSTAPAPER_CONSUMER_ID = os.environ.get('INSTAPAPER_CONSUMER_ID')
INSTAPAPER_CONSUMER_SECRET = os.environ.get('INSTAPAPER_CONSUMER_SECRET')


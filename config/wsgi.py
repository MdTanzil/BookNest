import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Serve user-uploaded media (book covers, category/author images) on Vercel.
# Vercel serves collected static files from its CDN itself, but media files
# are not collected, so WhiteNoise serves them from MEDIA_ROOT. Local
# `runserver` is unaffected: it serves media itself while DEBUG is True.
from django.conf import settings
from whitenoise import WhiteNoise

application = WhiteNoise(application, root=settings.MEDIA_ROOT, prefix='media/')

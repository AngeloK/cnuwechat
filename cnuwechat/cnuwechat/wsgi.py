"""
WSGI config for cnuwechat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnuwechat.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


def get_access_token():
	print 'get access_token'


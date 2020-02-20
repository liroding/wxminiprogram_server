"""
WSGI config for wxsmallproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from os.path import join,dirname,abspath 

PROJECT_DIR = dirname(dirname(abspath(__file__))) 
"""add by liro """

import sys
sys.path.insert(0,PROJECT_DIR) 
"""add by liro """


os.environ["DJANGO_SETTINGS_MODULE"]= "wxminiprogram.settings"

from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()

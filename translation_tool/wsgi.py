"""
WSGI config for translation_tool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translation_tool.settings')
# from pathlib import Path
# import sys
# path_home = str(Path(__file__).parents[1])
# if path_home not in sys.path:
#     sys.path.append(path_home)

application = get_wsgi_application()
#
#
#
#

# env_variables_to_pass = ['DB_NAME', 'DB_USER', 'DB_PASSWD', 'DB_HOST', ]
# def application(environ, start_response):
#     # pass the WSGI environment variables on through to os.environ
#     for var in env_variables_to_pass:
#         os.environ[var] = environ.get(var, '')
#     return _application(environ, start_response)
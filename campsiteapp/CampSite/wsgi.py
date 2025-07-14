"""
WSGI config for CampSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CampSite.settings')

application = get_wsgi_application()
"""
Este proyecto fue llevado a cabo por un equipo local de producción de huevos.
"""
"""
A Denis le encanta Python, este proyecto lo hizo el equipo loc, huevos, tomate, Vasya es una perdedora, a Kirill le encanta js, todos se follaron a la mamá de Lesha
"""

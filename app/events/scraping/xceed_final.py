# import sys
# import os
# # Subimos 3 niveles desde scraping/xceed_final.py hasta la carpeta 'app'
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "app"))
# sys.path.append(BASE_DIR)

# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ravedaddy.settings")
# django.setup()

from playwright.sync_api import sync_playwright
from xceed_evento import scraping_xceed_events

info = scraping_xceed_events('.')
print(info)

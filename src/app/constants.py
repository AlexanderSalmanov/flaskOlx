import os
import re


TEMPLATE_FOLDER = os.path.abspath("./templates")
CATEGORY_NAMES = [
    "transport",
    "nedvizhimost",
    "dopomoga",
    "detskiy-mir",
    "rabota",
    "zhivotnye",
    "elektronika",
    "moda-i-stil",
]

BASE_URL = "https://www.olx.ua/uk"
SEARCH_URL_TEMPLATE = "list/q-{}".format  # NOTE: insert slugified search query!
PAGE_NUMBER = "?page={}".format

RE_PATTERN = re.compile(r'window\.__PRERENDERED_STATE__\s*=\s*("(?:\\.|[^"])*");')
ADS_INTERNAL_KEYS = [
    "id",
    "user",
    "title",
    "description",
    "status",
    "price",
    "createdTime",
    "location",
    "photos",
]

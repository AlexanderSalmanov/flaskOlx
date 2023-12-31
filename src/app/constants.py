import os
import re


# TEMPLATE_FOLDER = os.path.abspath("./templates")
CATEGORY_NAMES = [
    ("Транспорт", "transport"),
    ("Нерухомість", "nedvizhimost"),
    ("Допомога", "dopomoga"),
    ("Дитячий світ", "detskiy-mir"),
    ("Робота", "rabota"),
    ("Тварини", "zhivotnye"),
    ("Електроніка", "elektronika"),
    ("Мода і стиль", "moda-i-stil"),
]
# Reversed pair of category values and names to be passed to the template
CATEGORY_NAMES_BY_ROUTE = {value: key for key, value in dict(CATEGORY_NAMES).items()}

# OLX URL routing constants
BASE_URL = "https://www.olx.ua/uk"
SEARCH_URL_TEMPLATE = "list/q-{}".format  # NOTE: insert slugified search query!
CATEGORY_SEARCH_URL_TEMPLATE = "{}/q-{}".format
PAGE_NUMBER = "?page={}".format

# Regex patterns and scraping constants
RE_PATTERN = re.compile(r'window\.__PRERENDERED_STATE__\s*=\s*("(?:\\.|[^"])*");')
ADS_INTERNAL_KEYS = [
    "id",
    "url",
    "user",
    "title",
    "description",
    "status",
    "price",
    "createdTime",
    "location",
    "photos",
]

import json
import requests
import logging
from bs4 import BeautifulSoup
from app import constants


logger = logging.getLogger(__name__)


class PageParser:
    def __init__(self, **init_params):
        self.category_name = init_params.get("category_name")
        self.page_number = init_params.get("page_number", 1)
        self.search_keyword = init_params.get("search_keyword")
        self.request_url = self._build_request_url()
        self._get_response()
        self._get_soup()

    def _build_request_url(self):
        logger.info(f"Building request url for {self.category_name}")
        # TODO: build url separately for search and category (+ add search and category mixed url)
        return (
            (
                f"{constants.BASE_URL}/{self.category_name}/{constants.PAGE_NUMBER(self.page_number)}"
            )
            if not self.search_keyword is not None
            else (
                f"{constants.BASE_URL}/{constants.SEARCH_URL_TEMPLATE(self.search_keyword)}/{constants.PAGE_NUMBER(self.page_number)}"
            )
        )

    def _get_response(self):
        logger.info(f"Fetching ads from {self.request_url}")
        self.response = requests.get(self.request_url)

    def _get_soup(self):
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def _parse_page_content(self):
        script_tag_content = self.soup.find("script", id="olx-init-config")
        match = constants.RE_PATTERN.search(script_tag_content.string)
        if match:
            olx_internal_data = json.loads(match.group(1))
            data_json = json.loads(olx_internal_data)
            listing_data = data_json["listing"]["listing"]
            num_pages = int(listing_data["totalPages"])
            ads_data = listing_data["ads"]
            return num_pages, ads_data

        return None, None

    def get_page_data(self):
        logger.info(f"Retrieving serialized data from OLX page...")
        num_pages, ads_data = self._parse_page_content()
        return num_pages, ads_data

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
        return (
            self._build_category_request_url()
            if not self.search_keyword is not None
            else self._build_search_request_url()
        )

    def _build_category_request_url(self):
        return f"{constants.BASE_URL}/{self.category_name}/{constants.PAGE_NUMBER(self.page_number)}"

    def _build_search_request_url(self):
        return (
            f"{constants.BASE_URL}/{constants.SEARCH_URL_TEMPLATE(self.search_keyword)}/{constants.PAGE_NUMBER(self.page_number)}"
            if self.category_name == "all"
            else f"{constants.BASE_URL}/{constants.CATEGORY_SEARCH_URL_TEMPLATE(self.category_name, self.search_keyword)}{constants.PAGE_NUMBER(self.page_number)}"
        )

    def _get_response(self):
        logger.info(f"Fetching ads from {self.request_url}")
        try:
            self.response = requests.get(self.request_url)
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Error on fetching data from {self.request_url}")
            self.response = None

    def _get_soup(self):
        if self.response:
            self.soup = BeautifulSoup(self.response.text, "html.parser")
        else:
            self.soup = None
            logger.warning(
                "Failed to instantiate BeautifulSoup object. "
                f"Most likely, no content was fetched from {self.request_url}"
            )

    def _parse_page_content(self):
        if not self.soup:
            logger.warning(
                f"Failed to parse page {self.request_url} content. Aborting..."
            )
            return None, None
        script_tag_content = self.soup.find("script", id="olx-init-config")
        match = constants.RE_PATTERN.search(script_tag_content.string)
        if match:
            olx_internal_data = json.loads(match.group(1))
            data_json = json.loads(olx_internal_data)
            listing_data = data_json["listing"]["listing"]
            num_pages = int(listing_data["totalPages"])
            ads_data = listing_data["ads"]
            return num_pages, ads_data

        logger.info(f"No serialized data found on {self.request_url}")
        return None, None

    def get_page_data(self):
        logger.info(f"Retrieving serialized data from OLX page...")
        num_pages, ads_data = self._parse_page_content()
        return num_pages, ads_data

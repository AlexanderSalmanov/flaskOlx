import logging
from flask import Blueprint, render_template, request

from app.services.advert_builder import AdvertBuilder
from app.services.parse_page import PageParser
from models.commerce import Advert, Category

from extensions import db
from app import constants


bp = Blueprint("categories", __name__, url_prefix="/categories")
logger = logging.getLogger(__name__)


@bp.route("/<string:category_name>")
def category_adverts(category_name):
    page_number = int(request.args.get("page", 1))
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category.create(name=category_name)
    category_display_name = constants.CATEGORY_NAMES_BY_ROUTE.get(category_name)

    # Check if there are existing ads for the given page number
    # If there are - pull them directly from the database and render them
    existing_ads = Advert.query.filter_by(
        category=category, page_number=page_number
    ).all()

    if existing_ads:
        logger.info(f"Found {len(existing_ads)} existing ads for page {page_number}")
        ad_builder = AdvertBuilder(existing_ads)
        ads_data_cleaned = ad_builder.get_serialized_ads(existing_ads)
        return render_template(
            "categories/category.html",
            category_name=category_display_name,
            ads_data=ads_data_cleaned,
            num_pages=category.num_pages,
            current_page=page_number,
        )

    logger.info(f"No existing ads found for page {page_number}")

    # If there are no existing ads for the given page number,
    # instantiate pageParser object and retrieve the data from the page
    page_parser = PageParser(category_name=category_name, page_number=page_number)
    num_pages, ads_data = page_parser.get_page_data()

    if not category.num_pages or category.num_pages != num_pages:
        category.update(num_pages=num_pages)

    # Instantiate AdvertBuilder object and build the ads from OLX response
    ads_builder = AdvertBuilder(ads_data)
    ads_data_cleaned = ads_builder.get_serialized_ads(ads_data)

    ads_builder.create_adverts(db, category=category, page_number=page_number)

    logger.info(
        f"Next time you visit this page, the ads will be loaded from the database"
    )

    return render_template(
        "categories/category.html",
        category_name=category_display_name,
        ads_data=ads_data_cleaned,
        num_pages=num_pages,
        current_page=page_number,
        target_url=f"/categories/{category_name}",
    )

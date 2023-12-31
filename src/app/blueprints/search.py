import logging
from flask import Blueprint, render_template, request

from app.services.advert_builder import AdvertBuilder
from app.services.parse_page import PageParser
from models.commerce import Search, Advert
from extensions import db
from app import constants


bp = Blueprint("search", __name__, url_prefix="/search")
logger = logging.getLogger(__name__)


@bp.route("/", methods=["GET"])
def search():
    search_input = request.args.get("keyword-search")
    page_number = int(request.args.get("page", 1))
    category = request.args.get("category-search", "all")

    if "?" in search_input:
        split_input = search_input.split("?")
        search_input = split_input[0].strip().lower().replace(" ", "-")
        category = split_input[1].strip().split("=")[-1].lower().replace(" ", "-")
        page_number = int(split_input[-1].strip().split("=")[1])

    target_url = f"/search/?keyword-search={search_input}?category-search={category}"

    # Explicitly get the human-readable category name for the template
    category_display_name = (
        category
        if category == "all"
        else constants.CATEGORY_NAMES_BY_ROUTE.get(category)
    )

    # Check if there are existing ads for the given search request;
    # If there are - pull them directly from the database and render them
    search_obj = Search.query.filter_by(keyword=search_input).first()
    if not search_obj:
        search_obj = Search.create(keyword=search_input)

    existing_ads = Advert.query.filter_by(
        search=search_obj, page_number=page_number
    ).all()

    if existing_ads:
        logger.info(
            f"Found {len(existing_ads)} existing ads for query {search_input}; page {page_number}"
        )
        ad_builder = AdvertBuilder(existing_ads)
        ads_data_cleaned = ad_builder.get_serialized_ads(existing_ads)
        return render_template(
            "search/search.html",
            **{
                "search_input": search_input,
                "ads_data": ads_data_cleaned,
                "num_pages": search_obj.num_pages,
                "current_page": page_number,
                "target_url": target_url,
                "category_name": category_display_name,
            },
        )

    # Instantiate pageParser object and retrieve the data from the page
    page_parser = PageParser(
        search_keyword=search_input, page_number=page_number, category_name=category
    )
    num_pages, ads_data = page_parser.get_page_data()

    if not num_pages or not ads_data:
        return render_template(
            "search/not_found.html",
            **dict(
                search_input=search_input,
                category_name=category,
            ),
        )

    if not search_obj.num_pages or search_obj.num_pages != num_pages:
        search_obj.update(num_pages=num_pages)

    # Instantiate AdvertBuilder object and build the ads from OLX response;
    # Save new ads to the database
    ads_builder = AdvertBuilder(ads_data)
    ads_data_cleaned = ads_builder.get_serialized_ads(ads_data)
    ads_builder.create_adverts(db, search=search_obj, page_number=page_number)

    return render_template(
        "search/search.html",
        **{
            "search_input": search_input,
            "ads_data": ads_data_cleaned,
            "num_pages": num_pages,
            "current_page": page_number,
            "target_url": target_url,
            "category_name": category_display_name,
        },
    )

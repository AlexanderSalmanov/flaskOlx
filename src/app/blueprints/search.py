import logging
from flask import Blueprint, render_template, request

from app.services.advert_builder import AdvertBuilder
from app.services.parse_page import PageParser
from models.commerce import Search, Advert
from extensions import db


bp = Blueprint("search", __name__, url_prefix="/search")
logger = logging.getLogger(__name__)


@bp.route("/", methods=["GET"])
def search():
    search_input = request.args.get("keyword-search")
    page_number = int(request.args.get("page", 1))

    if "?" in search_input:
        split_input = search_input.split("?")
        search_input = split_input[0].strip().lower().replace(" ", "-")
        page_number = int(split_input[-1].strip().split("=")[1])

    category = request.args.get("category-search", "all")  # TODO: add categories
    target_url = f"/search/?keyword-search={search_input}?category-search={category}"

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
            },
        )

    page_parser = PageParser(search_keyword=search_input, page_number=page_number)
    num_pages, ads_data = page_parser.get_page_data()
    if not search_obj.num_pages or search_obj.num_pages != num_pages:
        search_obj.update(num_pages=num_pages)

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
        },
    )

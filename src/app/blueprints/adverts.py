from flask import Blueprint, render_template

from models.commerce import Advert


bp = Blueprint("adverts", __name__, url_prefix="/adverts")


@bp.route("/<advert_id>")
def advert(advert_id):
    advert = Advert.query.filter_by(id=advert_id).first()
    if advert:
        return render_template(
            "adverts/ad_single.html",
            **dict(
                advert=advert
            )
        )
    return render_template("search/not_found.html", search_input=advert_id)

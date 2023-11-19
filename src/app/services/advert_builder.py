import logging
import sqlalchemy
from app import constants
from psycopg2.errors import UniqueViolation
from datetime import datetime


from models.commerce import Advert


class AdvertBuilder:
    """
    Utility class for building Advert objects from raw data.
    Builds objects from two states:
        - on first page visit (from JSON data);
        - on subsequent page visits (from the database).
    """
    def __init__(self, source_ads):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing AdvertBuilder")
        self.source_ads = source_ads
        self.serialized_ads: list = []

    def get_serialized_ads(self, ads):
        self._build(ads)
        return self.serialized_ads

    def create_adverts(self, db, **kwargs):
        self._create_advert_objects(db, **kwargs)

    def _build(self, ads: list[dict] | list[Advert]):
        self.serialized_ads = [self._serialize_ad_entry(ad) for ad in ads]

    def _serialize_ad_entry(self, ad_entry: dict | Advert) -> dict:
        """
        Retrieve only the necessary keys from the raw advertisement data.

        If the ad_entry is an Advert object, convert it to a dictionary.
        Otherwise, assume it's a dictionary and proceed.
        """
        if isinstance(ad_entry, Advert):
            ad_entry = ad_entry.__dict__

        serialized_ad = {
            k: v for k, v in ad_entry.items() if k in constants.ADS_INTERNAL_KEYS
        }
        return self._clean_ad_description(serialized_ad)
    
    def _clean_ad_description(self, ad) -> dict:
        """
        Remove extra HTML elements (e.g. <br />) tags from the description.
        """
        cleaned_ad_description = ad.get("description").replace("<br />", "")
        ad["description"] = cleaned_ad_description
        return ad

    def _create_advert_objects(self, db, **kwargs):
        """
        Create Advert objects from the serialized ads.
        Replaces some keys from raw data to match the signature of the Advert model.
        """
        created_objs = 0
        for ad in self.serialized_ads:
            ad["author"] = ad["user"]
            del ad["user"]
            ad["page_number"] = kwargs.get("page_number")
            ad["created_at"] = datetime.fromisoformat(ad["createdTime"])
            del ad["createdTime"]

            try:
                # NOTE: consider some analogy of Django's bulk_create (?)
                Advert.create(
                    category=kwargs.get("category", None),
                    search=kwargs.get("search", None),
                    **ad,
                )
            except (UniqueViolation, sqlalchemy.exc.IntegrityError):
                print(f"Skipping duplicate ad with id {ad['id']}")
                db.session.rollback()
                continue
            else:
                created_objs += 1

        self.logger.info(f"Created {created_objs} new Advert objects")

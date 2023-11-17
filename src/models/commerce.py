from sqlalchemy.dialects.postgresql import JSON, ARRAY, UUID

from helpers import CRUDMixin, DateMixin
from extensions import db
from enums import Status


class Category(db.Model, CRUDMixin, DateMixin):
    name = db.Column(db.String(64), nullable=False, unique=True)
    num_pages = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Category {self.name}>"


class Search(db.Model, CRUDMixin, DateMixin):
    keyword = db.Column(db.String(128), nullable=False)
    num_results = db.Column(db.Integer, nullable=False, default=0)
    num_pages = db.Column(db.Integer, nullable=False, default=1)
    category_uuid = db.Column(UUID, db.ForeignKey("category.uuid"), nullable=True)
    category = db.relationship("Category", backref=db.backref("searches", lazy=True))

    def __repr__(self):
        return f"<Search {self.keyword}>"


class Advert(db.Model, CRUDMixin, DateMixin):
    external_id = db.Column(db.String(64), unique=True, nullable=False)
    author = db.Column(JSON, default={})
    title = db.Column(db.String(192), nullable=False)
    category_uuid = db.Column(UUID, db.ForeignKey("category.uuid"), nullable=True)
    category = db.relationship(
        "Category", backref=db.backref("advertisements", lazy=True)
    )
    search_uuid = db.Column(UUID, db.ForeignKey("search.uuid"), nullable=True)
    search = db.relationship("Search", backref=db.backref("advertisements", lazy=True))
    description = db.Column(db.Text, nullable=True, default="Sample advert description")
    status = db.Column(db.String(50), default=Status.ACTIVE.value, nullable=False)
    price = db.Column(JSON, default={})
    location = db.Column(JSON, default={})
    photos = db.Column(ARRAY(db.String(512)), default=[], nullable=True)
    page_number = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Advert {self.title}>"

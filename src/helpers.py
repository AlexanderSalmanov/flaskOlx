import uuid
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from datetime import datetime

from extensions import db


class CRUDMixin:
    __table_args__ = {"extend_existing": True}

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @classmethod
    def get_by_uuid(cls, uuid):
        if isinstance(uuid, str):
            uuid = uuid.UUID(uuid)
        return cls.query.get(uuid)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class DateMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        nullable=False,
    )


class AutoEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    @classmethod
    def get_choice_pair_values(cls):
        return [(item.value, item.name) for item in cls]

from datetime import datetime

import arrow
from mongoengine import *


class Base(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    created_at = DateTimeField(
        default=datetime.now
    )

    updated_at = DateTimeField(
        default=datetime.now
    )

    @property
    def id_str(self):
        return str(self.id)

    @property
    def created_at_iso8601(self):
        return arrow.get(self.created_at).isoformat()

    @property
    def updated_at_iso8610(self):
        return arrow.get(self.updated_at).isoformat()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        return super(Base, self).save(*args, **kwargs)

    def update(self, **kwargs):
        kwargs.update({
            'updated_at': datetime.now()
        })

        return super(Base, self).update(**kwargs)

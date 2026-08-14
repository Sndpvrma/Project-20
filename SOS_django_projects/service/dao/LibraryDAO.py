from service.dao.BaseDAO import BaseDAO
from service.models import Library


class LibraryDAO(BaseDAO):
    def get_Unique(self):
        return ["library_id"]

    def get_model(self):
        return Library

    def populate(self, obj):
        return obj
from service.dao.BaseDAO import BaseDAO
from service.models import Vendor


class VendorDAO(BaseDAO):
    def get_Unique(self):
        return ["vendor_id"]

    def get_model(self):
        return Vendor

    def populate(self, obj):
        return obj
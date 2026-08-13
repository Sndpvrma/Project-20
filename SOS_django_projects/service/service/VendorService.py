from service.dao.VendorDAO import VendorDAO
from service.service.BaseService import BaseService


class VendorService(BaseService):
    def get_dao(self):
        return VendorDAO()
from service.dao.VehicleDAO import VehicleDAO
from service.service.BaseService import BaseService


class VehicleService(BaseService):
    def get_dao(self):
        return VehicleDAO()
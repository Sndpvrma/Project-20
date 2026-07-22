from service.dao.ParkingDAO import ParkingDAO
from service.service.BaseService import BaseService


class ParkingService(BaseService):
    def get_dao(self):
        return ParkingDAO()
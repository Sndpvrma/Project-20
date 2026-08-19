from service.dao.HotelDAO import HotelDAO
from service.service.BaseService import BaseService


class HotelService(BaseService):
    def get_dao(self):
        return HotelDAO()
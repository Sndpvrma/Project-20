from service.dao.RoomDAO import RoomDAO
from service.service.BaseService import BaseService


class RoomService(BaseService):
    def get_dao(self):
        return RoomDAO()
from service.dao.DroneDAO import DroneDAO
from service.service.BaseService import BaseService


class DroneService(BaseService):
    def get_dao(self):
        return DroneDAO()
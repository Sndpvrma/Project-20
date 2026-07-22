from service.dao.BaseDAO import BaseDAO
from service.models import Parking


class ParkingDAO(BaseDAO):
    def get_model(self):
        return Parking

    def get_Unique(self):
        return ["parking_id"]

    def populate(self, obj):
        return obj
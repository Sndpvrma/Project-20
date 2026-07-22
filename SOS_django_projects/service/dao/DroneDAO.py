from service.dao.BaseDAO import BaseDAO
from service.models import Drone


class DroneDAO(BaseDAO):
    def get_model(self):
        return Drone

    def get_Unique(self):
        return ['drone_id']

    def populate(self, obj):
        return obj
from service.dao.BaseDAO import BaseDAO
from service.models import Vehicle


class VehicleDAO(BaseDAO):
    def get_Unique(self):
        return ["vehicle_id"]

    def get_model(self):
        return Vehicle

    def populate(self, obj):
        return obj
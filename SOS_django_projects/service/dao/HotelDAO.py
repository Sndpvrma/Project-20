from service.dao.BaseDAO import BaseDAO
from service.models import Hotel


class HotelDAO(BaseDAO):
    def get_Unique(self):
        return ["hotel_id"]

    def get_model(self):
        return Hotel

    def populate(self, obj):
        return obj
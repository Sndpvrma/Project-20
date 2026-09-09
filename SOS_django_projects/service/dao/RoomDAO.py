from service.dao.BaseDAO import BaseDAO
from service.models import Room


class RoomDAO(BaseDAO):
    def get_Unique(self):
        return ["room_id"]

    def get_model(self):
        return Room

    def populate(self, obj):
        return obj
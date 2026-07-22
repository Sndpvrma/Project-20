from service.dao.BaseDAO import BaseDAO
from service.models import WeatherAlert


class WeatherAlertDAO(BaseDAO):
    def get_Unique(self):
        return ["alert_id"]

    def get_model(self):
        return WeatherAlert

    def populate(self, obj):
        return obj
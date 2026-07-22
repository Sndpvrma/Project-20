from service.dao.WeatherAlertDAO import WeatherAlertDAO
from service.service.BaseService import BaseService


class WeatherAlertService(BaseService):
    def get_dao(self):
        return WeatherAlertDAO()
from service.dao.DoctorDAO import DoctorDAO
from service.service.BaseService import BaseService


class DoctorService(BaseService):
    def get_dao(self):
        return DoctorDAO()
from service.dao.BaseDAO import BaseDAO
from service.models import Doctor


class DoctorDAO(BaseDAO):
    def get_Unique(self):
        return ["doctor_id"]

    def get_model(self):
        return Doctor

    def populate(self, obj):
        return obj
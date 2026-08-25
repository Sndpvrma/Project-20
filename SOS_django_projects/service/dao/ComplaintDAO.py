from service.dao.BaseDAO import BaseDAO
from service.models import Complaint


class ComplaintDAO(BaseDAO):
    def get_Unique(self):
        return ["complaint_id"]

    def get_model(self):
        return Complaint

    def populate(self, obj):
        return obj
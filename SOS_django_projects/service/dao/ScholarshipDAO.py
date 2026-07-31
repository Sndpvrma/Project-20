from service.dao.BaseDAO import BaseDAO
from service.models import Scholarship


class ScholarshipDAO(BaseDAO):
    def get_model(self):
        return Scholarship

    def get_Unique(self):
        return ['scholarship_id']

    def populate(self, obj):
        return obj
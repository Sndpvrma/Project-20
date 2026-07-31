from service.dao.BaseDAO import BaseDAO
from service.models import Insurance


class InsuranceDAO(BaseDAO):
    def get_model(self):
        return Insurance

    def get_Unique(self):
        return ['policy_id']

    def populate(self, obj):
        return obj
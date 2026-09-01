from service.dao.BaseDAO import BaseDAO
from service.models import BankAccount


class BankAccountDAO(BaseDAO):
    def get_Unique(self):
        return ["account_number"]

    def get_model(self):
        return BankAccount

    def populate(self, obj):
        return obj
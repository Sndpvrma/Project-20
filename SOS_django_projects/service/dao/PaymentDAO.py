from service.dao.BaseDAO import BaseDAO
from service.models import Payment


class PaymentDAO(BaseDAO):
    def get_Unique(self):
        return ["payment_id"]

    def get_model(self):
        return Payment

    def populate(self, obj):
        return obj
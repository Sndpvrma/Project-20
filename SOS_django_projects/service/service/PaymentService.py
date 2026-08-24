from service.dao.PaymentDAO import PaymentDAO
from service.service.BaseService import BaseService


class PaymentService(BaseService):
    def get_dao(self):
        return PaymentDAO()
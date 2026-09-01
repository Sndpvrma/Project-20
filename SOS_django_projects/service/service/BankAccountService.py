from service.dao.BankAccountDAO import BankAccountDAO
from service.service.BaseService import BaseService


class BankAccountService(BaseService):
    def get_dao(self):
        return BankAccountDAO()
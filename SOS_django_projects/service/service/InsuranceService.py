from service.dao.InsuranceDAO import InsuranceDAO
from service.service.BaseService import BaseService


class InsuranceService(BaseService):
    def get_dao(self):
        return InsuranceDAO()
from service.dao.ScholarshipDAO import ScholarshipDAO
from service.service.BaseService import BaseService


class ScholarshipService(BaseService):
    def get_dao(self):
        return ScholarshipDAO()
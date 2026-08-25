from service.dao.ComplaintDAO import ComplaintDAO
from service.service.BaseService import BaseService


class ComplaintService(BaseService):
    def get_dao(self):
        return ComplaintDAO()
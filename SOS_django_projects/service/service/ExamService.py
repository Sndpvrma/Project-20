from service.dao.ExamDAO import ExamDAO
from service.service.BaseService import BaseService


class ExamService(BaseService):
    def get_dao(self):
        return ExamDAO()
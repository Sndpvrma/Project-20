from service.dao.BaseDAO import BaseDAO
from service.models import Exam


class ExamDAO(BaseDAO):
    def get_model(self):
        return Exam

    def get_Unique(self):
        return ['exam_id']

    def populate(self, obj):
        return obj
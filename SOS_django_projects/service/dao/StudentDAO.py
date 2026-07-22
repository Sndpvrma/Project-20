from service.models import Student, College
from .BaseDAO import BaseDAO


class StudentDAO(BaseDAO):

    def get_model(self):
        return Student

    def get_Unique(self):
        return None

    def populate(self, obj):
        try:
            college = College.objects.get(id=obj.college_ID)
            obj.collegeName = college.name
        except College.DoesNotExist:
            obj.collegeName = ""
        return obj

from service.models import Marksheet, Student, Subject
from .BaseDAO import BaseDAO


class MarksheetDAO(BaseDAO):

    def get_model(self):
        return Marksheet

    def get_Unique(self):
        return ["rollNumber"]

    def populate(self, obj):
        if obj.student_id:
            try:
                student = Student.objects.get(id=obj.student_id)
                obj.student_Name = student.firstName + " " + student.lastName
            except Student.DoesNotExist:
                obj.student_Name = ""
        else:
            obj.student_Name = ""
        return obj

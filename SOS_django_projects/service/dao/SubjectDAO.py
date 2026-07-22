from service.models import Subject, Course
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class SubjectDAO(BaseDAO):

    def get_model(self):
        return Subject

    def get_Unique(self):
        return ["name"]

    def populate(self, obj):
        try:
            course = Course.objects.get(id=obj.course_ID)
            obj.courseName = course.name
        except Course.DoesNotExist:
            obj.courseName = ""
        return obj

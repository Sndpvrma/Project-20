from service.models import Faculty, College, Course, Subject
from .BaseDAO import BaseDAO


class FacultyDAO(BaseDAO):

    def get_model(self):
        return Faculty

    def get_Unique(self):
        return None

    def populate(self, obj):
        try:
            college = College.objects.get(id=obj.college_ID)
            obj.collegeName = college.name
        except College.DoesNotExist:
            obj.collegeName = ""
        try:
            course = Course.objects.get(id=obj.course_ID)
            obj.courseName = course.name
        except Course.DoesNotExist:
            obj.courseName = ""
        try:
            subject = Subject.objects.get(id=obj.subject_ID)
            obj.subjectName = subject.name
        except Subject.DoesNotExist:
            obj.subjectName = ""
        return obj

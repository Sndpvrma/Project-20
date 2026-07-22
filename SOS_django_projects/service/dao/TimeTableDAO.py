from service.models import TimeTable, Course, Subject
from .BaseDAO import BaseDAO


class TimeTableDAO(BaseDAO):

    def get_model(self):
        return TimeTable

    def get_Unique(self):
        return None

    def populate(self, obj):
        try:
            course = Course.objects.get(id=obj.course_id)
            obj.course_name = course.name
        except Course.DoesNotExist:
            obj.course_name = ""
        try:
            subject = Subject.objects.get(id=obj.subject_id)
            obj.subject_name = subject.name
        except Subject.DoesNotExist:
            obj.subject_name = ""
        return obj

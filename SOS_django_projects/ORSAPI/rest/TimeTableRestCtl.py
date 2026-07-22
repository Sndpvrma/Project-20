from rest_framework.views import APIView
from rest_framework.response import Response
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import TimeTable
from service.Serializers import TimeTableSerializers
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from service.utility.DataValidator import DataValidator


class TimeTableRestCtl(BaseRestCtl):
    def get_model(self):
        return TimeTable

    def get_service(self):
        return TimeTableService()

    def get_serializer_class(self):
        return TimeTableSerializers

    def input_validation(self, data):
        errors = {}

        exam_date = data.get("exam_date", "")
        exam_time = data.get("exam_time", "")
        semester = data.get("semester", "")
        course_id = data.get("course_id", 0)
        subject_id = data.get("subject_id", 0)

        if DataValidator.isNull(exam_date):
            errors["exam_date"] = "Exam Date cannot be null"

        if DataValidator.isNull(exam_time) or str(exam_time) == "0":
            errors["exam_time"] = "Exam Time cannot be null"

        if DataValidator.isNull(semester) or str(semester) == "0":
            errors["semester"] = "Semester cannot be null"

        if DataValidator.isNull(course_id) or str(course_id) == "0":
            errors["course_id"] = "Course cannot be null"

        if DataValidator.isNull(subject_id) or str(subject_id) == "0":
            errors["subject_id"] = "Subject cannot be null"

        return errors


class TimeTablePreloadRestCtl(APIView):
    EXAM_TIMES = [
        "08:00 AM to 11:00 AM",
        "12:00 PM to 03:00 PM",
        "04:00 PM to 07:00 PM",
    ]
    SEMESTERS = ["1", "2", "3", "4", "5", "6", "7", "8"]

    def get(self, _request):
        courses = [{"id": c.get_key(), "value": c.get_value()} for c in CourseService().search({})]
        subjects = [{"id": s.get_key(), "value": s.get_value()} for s in SubjectService().search({})]
        data = {
            "exam_times": self.EXAM_TIMES,
            "semesters": self.SEMESTERS,
            "courses": courses,
            "subjects": subjects,
        }
        return Response({"error": False, "message": "", "data": data})

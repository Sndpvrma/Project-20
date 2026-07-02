from datetime import datetime
from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import TimeTable
from service.service.time_table_service import TimeTableService
from service.service.course_service import CourseService
from service.service.subject_service import SubjectService
from ..utility.html_utility import HtmlUtility
from ..utility.data_validator import DataValidator


class TimeTableCtl(BaseCtl):

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["exam_date"] = request_form.get("exam_date", "").strip()
        self.form["exam_time"] = request_form.get("exam_time", "").strip()
        self.form["semester"] = request_form.get("semester", "").strip()
        self.form["course_id"] = request_form.get("course_id", 0)
        self.form["subject_id"] = request_form.get("subject_id", 0)

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.exam_date = (
            datetime.strptime(self.form.get("exam_date"), "%Y-%m-%d").date()
            if self.form.get("exam_date")
            else None
        )
        obj.exam_time = self.form.get("exam_time", "")
        obj.semester = self.form.get("semester", "")

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""

        subject_id = int(self.form.get("subject_id") or 0)
        obj.subject_id = subject_id

        subject = SubjectService().get(subject_id) if subject_id > 0 else None
        obj.subject_name = subject.name if subject else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["exam_date"] = obj.exam_date.strftime("%Y-%m-%d") if obj.exam_date else ""
        self.form["exam_time"] = obj.exam_time
        self.form["semester"] = obj.semester

        self.form["course_id"] = int(obj.course_id) if obj.course_id else 0
        self.form["subject_id"] = int(obj.subject_id) if obj.subject_id else 0

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.is_null(self.form.get("exam_date")):
            input_error["exam_date"] = "Exam Date can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("exam_time")) or self.form.get("exam_time") == "0":
            input_error["exam_time"] = "Exam Time can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("semester")) or self.form.get("semester") == "0":
            input_error["semester"] = "Semester can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("course_id")) or self.form.get("course_id") == "0":
            input_error["course_id"] = "Course can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("subject_id")) or self.form.get("subject_id") == "0":
            input_error["subject_id"] = "Subject can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def preload(self, request):
        exam_time_list = [
            "08:00 AM to 11:00 AM",
            "12:00 PM to 03:00 PM",
            "04:00 PM to 07:00 PM"
        ]
        semester_list = ["1", "2", "3", "4", "5", "6", "7", "8", ]
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

        self.preload_data["exam_time_select"] = HtmlUtility.get_list_from_list(
            "exam_time",
            self.form.get("exam_time"),
            exam_time_list
        )
        self.preload_data["semester_select"] = HtmlUtility.get_list_from_list(
            "semester",
            self.form.get("semester"),
            semester_list
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_id",
            int(self.form.get("course_id") or 0),
            course_list
        )
        self.preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subject_id",
            int(self.form.get("subject_id") or 0),
            subject_list
        )
        return self.preload_data

    def display(self, request, params={}):
        time_table_id = int(params.get("id", 0))

        if time_table_id > 0:
            time_table = self.get_service().get(time_table_id)
            self.model_to_form(time_table)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(
            exam_date=self.form.get('exam_date'),
            exam_time=self.form.get('exam_time'),
            semester=self.form.get('semester'),
            course_id=int(self.form.get('course_id') or 0),
            subject_id=int(self.form.get('subject_id') or 0)
        )

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "TimeTable already exist"

        else:
            timetable = self.form_to_model(TimeTable())
            self.get_service().save(timetable)

            self.form['id'] = timetable.id
            self.form['error'] = False
            self.form['message'] = "TimeTable added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "time_table.html"

    def get_service(self):
        return TimeTableService()

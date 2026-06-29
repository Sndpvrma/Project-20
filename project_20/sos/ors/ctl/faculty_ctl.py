from datetime import datetime
from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Faculty
from service.service.faculty_service import FacultyService
from service.service.college_service import CollegeService
from service.service.course_service import CourseService
from service.service.subject_service import SubjectService
from ..utility.html_utility import HtmlUtility
from ..utility.data_validator import DataValidator


class FacultyCtl(BaseCtl):

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("first_name", "").strip()
        self.form["last_name"] = request_form.get("last_name", "").strip()
        self.form["email"] = request_form.get("email", "").strip()
        self.form["password"] = request_form.get("password", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["gender"] = request_form.get("gender", "").strip()
        self.form["mobile_number"] = request_form.get("mobile_number", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["college_id"] = request_form.get("college_id", 0)
        self.form["course_id"] = request_form.get("course_id", 0)
        self.form["subject_id"] = request_form.get("subject_id", 0)

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.email = self.form.get("email", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.password = self.form.get("password", "")
        obj.gender = self.form.get("gender", "")
        obj.mobile_number = self.form.get("mobile_number", "")
        obj.address = self.form.get("address", "")

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""

        subject_id = int(self.form.get("subject_id") or 0)
        obj.subject_id = subject_id

        subject = SubjectService().get(subject_id) if subject_id > 0 else None
        obj.subject_name = subject.name if subject else ""

        return obj

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.is_null(self.form.get("first_name")):
            input_error["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("last_name")):
            input_error["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("email")):
            input_error["email"] = "Email can not be null"
            self.form["error"] = True

        # elif not DataValidator.is_email(self.form.get("email")):
        #     input_error["email"] = "Email must be a valid email address"
        #     self.form["error"] = True
        if DataValidator.is_null(self.form.get("password")):
            input_error["password"] = "Password can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("dob")):
            input_error["dob"] = "DOB can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("gender")) or self.form.get("gender") == "0":
            input_error["gender"] = "Gender can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True

        # elif not DataValidator.is_mobile_number(self.form.get("mobile_number")):
        #     input_error["mobile_number"] = "Mobile Number must be 10 digits"
        #     self.form["error"] = True

        if DataValidator.is_null(self.form.get("address")):
            input_error["address"] = "Address can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("college_id")) or self.form.get("college_id") == "0":
            input_error["college_id"] = "College can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("course_id")) or self.form.get("course_id") == "0":
            input_error["course_id"] = "Course can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("subject_id")) or self.form.get("subject_id") == "0":
            input_error["subject_id"] = "Subject can not be null"
            self.form["error"] = True

        return self.form.get("error", False)
    
    def preload(self, request):
        gender_list = ["Male", "Female", "Others"]
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )
        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_id",
            int(self.form.get("college_id") or 0),
            college_list
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
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(email=self.form.get('email', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Email already exist"

        else:
            faculty = self.form_to_model(Faculty())
            self.get_service().save(faculty)

            self.form['id'] = faculty.id
            self.form['error'] = False
            self.form['message'] = "Faculty added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "faculty.html"

    def get_service(self):
        return FacultyService()

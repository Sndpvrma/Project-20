from datetime import datetime
from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Student
from service.service.student_service import StudentService
from service.service.college_service import CollegeService
from ..utility.html_utility import HtmlUtility
from ..utility.data_validator import DataValidator


class StudentCtl(BaseCtl):

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("first_name", "").strip()
        self.form["last_name"] = request_form.get("last_name", "").strip()
        self.form["email"] = request_form.get("email", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["mobile_number"] = request_form.get("mobile_number", "").strip()
        self.form["college_id"] = request_form.get("college_id", 0)

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
        obj.mobile_number = self.form.get("mobile_number", "")

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""

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

        if DataValidator.is_null(self.form.get("dob")):
            input_error["dob"] = "Date Of Birth can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True
        # elif not DataValidator.is_mobile_number(self.form.get("mobile_number")):
        #     input_error["mobile_number"] = "Mobile Number must be 10 digits"
        #     self.form["error"] = True

        if DataValidator.is_null(self.form.get("college_id")) or self.form.get("college_id") == "0":
            input_error["college_id"] = "College can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def preload(self, request):
        college_list = CollegeService().search({})

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_id",
            int(self.form.get("college_id") or 0),
            college_list
        )
        return self.preload_data

    def display(self, request, params={}):
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    # def submit(self, request, params={}):
    #
    #     pk = int(self.form.get('id', 0))
    #
    #     duplicate = self.get_service().get_model().objects.filter(email=self.form.get('email', ''))
    #
    #     if pk > 0:
    #         duplicate = duplicate.exclude(id=pk)
    #
    #     if duplicate.exists():
    #         self.form['error'] = True
    #         self.form['message'] = "Student already exist"
    #     else:
    #         student = self.form_to_model(Student())
    #         self.get_service().save(student)
    #         self.form['id'] = student.id
    #         self.form['error'] = False
    #
    #         if pk > 0:
    #             self.form['message'] = "Student updated successfully"
    #         else:
    #             self.form['message'] = "Student added successfully..!!"
    #
    #     res = render(request, self.get_template(), {
    #         "form": self.form,
    #         "preload_data": self.preload(request)
    #     })
    #     return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(email=self.form.get('email', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Student already exist"

        else:
            student = self.form_to_model(Student())
            self.get_service().save(student)

            self.form['id'] = student.id
            self.form['error'] = False
            self.form['message'] = "Student added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "student.html"

    def get_service(self):
        return StudentService()

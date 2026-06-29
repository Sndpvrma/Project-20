from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Course
from service.service.course_service import CourseService
from ..utility.data_validator import DataValidator
from service.service.college_service import CollegeService

class CourseCtl(BaseCtl):

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["duration"] = request_form.get("duration", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["college_id"] = request_form.get("collegeId", 0)

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.name = self.form.get("name", "")
        obj.duration = self.form.get("duration", "")
        obj.description = self.form.get("description", "")

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""
        return obj

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.is_null(self.form.get("name")):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("duration")):
            input_error["duration"] = "Duration can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("description")):
            input_error["description"] = "Description can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("college_id")) or self.form.get("college_id") == "0":
            input_error["college_id"] = "College can not be null"
            self.form["error"] = True

        return self.form["error"]
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
    #     duplicate = self.get_service().get_model().objects.filter(name=self.form.get('name', ''))
    #
    #     if pk > 0:
    #         duplicate = duplicate.exclude(id=pk)
    #
    #     if duplicate.exists():
    #         self.form['error'] = True
    #         self.form['message'] = "Course already exist"
    #     else:
    #         course = self.form_to_model(Course())
    #         self.get_service().save(course)
    #         self.form['id'] = course.id
    #         self.form['error'] = False
    #
    #         if pk > 0:
    #             self.form['message'] = "Course updated successfully"
    #         else:
    #             self.form['message'] = "Course added successfully..!!"
    #
    #     res = render(request, self.get_template(), {
    #         "form": self.form,
    #         "preload_data": self.preload(request)
    #     })
    #     return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(name=self.form.get('name', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Course already exist"

        else:
            course = self.form_to_model(Course())
            self.get_service().save(course)

            self.form['id'] = course.id
            self.form['error'] = False
            self.form['message'] = "Course added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "course.html"

    def get_service(self):
        return CourseService()

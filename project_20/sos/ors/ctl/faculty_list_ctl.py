from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.faculty_service import FacultyService
from service.service.college_service import CollegeService
from service.service.course_service import CourseService
from service.service.subject_service import SubjectService
from ..utility.html_utility import HtmlUtility

class FacultyListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "collegeId",
            int(self.form.get("college_id") or 0),
            college_list
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId",
            int(self.form.get("course_id") or 0),
            course_list
        )
        self.preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subjectId",
            int(self.form.get("subject_id") or 0),
            subject_list
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["first_name"] = requestForm.get("first_name", "").strip()
        self.form["last_name"] = requestForm.get("last_name", "").strip()
        self.form["email"] = requestForm.get("email", "").strip()
        self.form["college_id"] = requestForm.get("college_id", 0)
        self.form["course_id"] = requestForm.get("course_id", 0)
        self.form["subject_id"] = requestForm.get("subject_id", 0)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = FacultyListCtl.count

        if request.POST['operation'] == "next":
            FacultyListCtl.count += 1
            self.form['page_no'] = FacultyListCtl.count
        if request.POST['operation'] == "previous":
            FacultyListCtl.count -= 1
            self.form['page_no'] = FacultyListCtl.count
        if request.POST['operation'] == "search":
            FacultyListCtl.count = 1
            self.form['page_no'] = FacultyListCtl.count
        if request.POST['operation'] == "delete":
            FacultyListCtl.count = 1
            self.form['page_no'] = FacultyListCtl.count
            for id in self.form['ids']:
                id = int(id)
                self.get_service().delete(id)
                self.form['error'] = False
                self.form['message'] = "Data has been deleted successfully"

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "faculty_list.html"

    def get_service(self):
        return FacultyService()
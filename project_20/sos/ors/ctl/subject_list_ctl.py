from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.subject_service import SubjectService
from service.service.course_service import CourseService
from ..utility.html_utility import HtmlUtility

class SubjectListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        course_list = CourseService().search({})

        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_id",
            int(self.form.get("course_id") or 0),
            course_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["course_id"] = request_form.get("course_id", 0)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = SubjectListCtl.count

        if request.POST['operation'] == "next":
            SubjectListCtl.count += 1
            self.form['page_no'] = SubjectListCtl.count
        if request.POST['operation'] == "previous":
            SubjectListCtl.count -= 1
            self.form['page_no'] = SubjectListCtl.count
        if request.POST['operation'] == "search":
            SubjectListCtl.count = 1
            self.form['page_no'] = SubjectListCtl.count
        if request.POST['operation'] == "delete":
            SubjectListCtl.count = 1
            self.form['page_no'] = SubjectListCtl.count
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
        return "subject_list.html"

    def get_service(self):
        return SubjectService()
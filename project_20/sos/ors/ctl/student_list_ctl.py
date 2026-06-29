from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.student_service import StudentService
from service.service.college_service import CollegeService
from ..utility.html_utility import HtmlUtility

class StudentListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        college_list = CollegeService().search({})

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_id",
            int(self.form.get("college_id") or 0),
            college_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("first_name", "").strip()
        self.form["last_name"] = request_form.get("last_name", "").strip()
        self.form["email"] = request_form.get("email", "").strip()
        self.form["college_id"] = request_form.get("college_id", 0)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = StudentListCtl.count

        if request.POST['operation'] == "next":
            StudentListCtl.count += 1
            self.form['page_no'] = StudentListCtl.count
        if request.POST['operation'] == "previous":
            StudentListCtl.count -= 1
            self.form['page_no'] = StudentListCtl.count
        if request.POST['operation'] == "search":
            StudentListCtl.count = 1
            self.form['page_no'] = StudentListCtl.count
        if request.POST['operation'] == "delete":
            StudentListCtl.count = 1
            self.form['page_no'] = StudentListCtl.count
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
        return "student_list.html"

    def get_service(self):
        return StudentService()
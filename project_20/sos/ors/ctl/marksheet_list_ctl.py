from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.marksheet_service import MarksheetService
from service.service.student_service import StudentService
from ..utility.html_utility import HtmlUtility

class MarksheetListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        student_list = StudentService().search({})

        self.preload_data["student_select"] = HtmlUtility.get_list_from_beans(
            "student_id",
            int(self.form.get("student_id") or 0),
            student_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["roll_number"] = request_form.get("roll_number", "").strip()
        self.form["name"] = request_form.get("name", "").strip()
        self.form["student_id"] = request_form.get("student_id", 0)

    def display(self, request, params={}):

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = MarksheetListCtl.count

        if request.POST['operation'] == "next":
            MarksheetListCtl.count += 1
            self.form['page_no'] = MarksheetListCtl.count
        if request.POST['operation'] == "previous":
            MarksheetListCtl.count -= 1
            self.form['page_no'] = MarksheetListCtl.count
        if request.POST['operation'] == "search":
            MarksheetListCtl.count = 1
            self.form['page_no'] = MarksheetListCtl.count
        if request.POST['operation'] == "delete":
            MarksheetListCtl.count = 1
            self.form['page_no'] = MarksheetListCtl.count
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
        return "marksheet_list.html"

    def get_service(self):
        return MarksheetService()
from django.shortcuts import render, redirect
from .base_ctl import BaseCtl
from service.service.course_service import CourseService


class CourseListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["duration"] = request_form.get("duration", "").strip()
        self.form["description"] = request_form.get("description", "").strip()

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = CourseListCtl.count

        if request.POST['operation'] == "next":
            CourseListCtl.count += 1
            self.form['page_no'] = CourseListCtl.count
        if request.POST['operation'] == "previous":
            CourseListCtl.count -= 1
            self.form['page_no'] = CourseListCtl.count
        if request.POST['operation'] == "search":
            CourseListCtl.count = 1
            self.form['page_no'] = CourseListCtl.count
        if request.POST['operation'] == "delete":
            CourseListCtl.count = 1
            self.form['page_no'] = CourseListCtl.count
            for id in self.form['ids']:
                id = int(id)
                self.get_service().delete(id)
                self.form['error'] = False
                self.form['message'] = "Data has been deleted successfully"

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "course_list.html"

    def get_service(self):
        return CourseService()
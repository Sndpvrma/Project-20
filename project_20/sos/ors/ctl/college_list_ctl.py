from django.shortcuts import render, redirect
from .base_ctl import BaseCtl
from service.service.college_service import CollegeService


class CollegeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["city"] = request_form.get("city", "").strip()
        self.form["state"] = request_form.get("state", "").strip()
        self.form["phone_number"] = request_form.get("phone_number", "").strip()

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = CollegeListCtl.count

        if request.POST['operation'] == "next":
            CollegeListCtl.count += 1
            self.form['page_no'] = CollegeListCtl.count
        if request.POST['operation'] == "previous":
            CollegeListCtl.count -= 1
            self.form['page_no'] = CollegeListCtl.count
        if request.POST['operation'] == "search":
            CollegeListCtl.count = 1
            self.form['page_no'] = CollegeListCtl.count
        if request.POST['operation'] == "delete":
            CollegeListCtl.count = 1
            self.form['page_no'] = CollegeListCtl.count
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
        return "college_list.html"

    def get_service(self):
        return CollegeService()
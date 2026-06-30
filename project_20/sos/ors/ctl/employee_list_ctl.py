from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.employee_service import EmployeeService

class EmployeeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["employee_name"] = request_form.get("employee_name", "").strip()
        self.form["department"] = request_form.get("department", "").strip()
        self.form["salary"] = request_form.get("salary", "").strip()
        self.form["joining_date"] = request_form.get("joining_date", " ").strip()
        self.form['ids'] = request_form.getlist('ids', None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = EmployeeListCtl.count

        if request.POST['operation'] == "next":
            EmployeeListCtl.count += 1
            self.form['page_no'] = EmployeeListCtl.count
        if request.POST['operation'] == "previous":
            EmployeeListCtl.count -= 1
            self.form['page_no'] = EmployeeListCtl.count
        if request.POST['operation'] == "search":
            EmployeeListCtl.count = 1
            self.form['page_no'] = EmployeeListCtl.count
        if request.POST['operation'] == "delete":
            EmployeeListCtl.count = 1
            self.form['page_no'] = EmployeeListCtl.count
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
        return "employee_list.html"

    def get_service(self):
        return EmployeeService()
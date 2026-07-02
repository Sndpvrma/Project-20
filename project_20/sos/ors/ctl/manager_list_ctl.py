from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.manager_service import ManagerService


class ManagerListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["manager_name"] = request_form.get("manager_name", "").strip()
        self.form["branch_name"] = request_form.get("branch_name", "").strip()
        self.form["contact_number"] = request_form.get("contact_number", "").strip()
        self.form['ids'] = request_form.getlist('ids', None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = ManagerListCtl.count

        if request.POST['operation'] == "next":
            ManagerListCtl.count += 1
            self.form['page_no'] = ManagerListCtl.count
        if request.POST['operation'] == "previous":
            ManagerListCtl.count -= 1
            self.form['page_no'] = ManagerListCtl.count
        if request.POST['operation'] == "search":
            ManagerListCtl.count = 1
            self.form['page_no'] = ManagerListCtl.count
        if request.POST['operation'] == "delete":
            ManagerListCtl.count = 1
            self.form['page_no'] = ManagerListCtl.count
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
        return "manager_list.html"

    def get_service(self):
        return ManagerService()
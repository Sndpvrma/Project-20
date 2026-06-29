from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.role_service import RoleService

class RoleListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form['ids'] = request_form.getlist('ids', None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = RoleListCtl.count

        if request.POST['operation'] == "next":
            RoleListCtl.count += 1
            self.form['page_no'] = RoleListCtl.count
        if request.POST['operation'] == "previous":
            RoleListCtl.count -= 1
            self.form['page_no'] = RoleListCtl.count
        if request.POST['operation'] == "search":
            RoleListCtl.count = 1
            self.form['page_no'] = RoleListCtl.count
        if request.POST['operation'] == "delete":
            RoleListCtl.count = 1
            self.form['page_no'] = RoleListCtl.count
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
        return "role_list.html"

    def get_service(self):
        return RoleService()
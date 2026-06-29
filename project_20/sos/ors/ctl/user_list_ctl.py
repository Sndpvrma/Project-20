from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.user_service import UserService
from service.service.role_service import RoleService
from ..utility.html_utility import HtmlUtility

class UserListCtl(BaseCtl):
    count = 1

    def preload(self, request):

        role_list = RoleService().search({})
        gender_list = ["Male", "Female"]

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "roleId",
            int(self.form.get("role_id") or 0),
            role_list
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )
        return self.preload_data

    def request_to_form(self, request_form):

        self.form["first_name"] = request_form.get("first_name", None)
        self.form["last_name"] = request_form.get("last_name", None)
        self.form["login"] = request_form.get("login", None)
        self.form["mobile_number"] = request_form.get("mobile_number", None)
        self.form["gender"] = request_form.get("gender", None)
        self.form["role_id"] = request_form.get("role_id", None)

    def display(self, request, params={}):

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "next":
            UserListCtl.count += 1
            self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "previous":
            UserListCtl.count -= 1
            self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "search":
            UserListCtl.count = 1
            self.form['page_no'] = UserListCtl.count
        if request.POST['operation'] == "delete":
            UserListCtl.count = 1
            self.form['page_no'] = UserListCtl.count
            for id in self.form['ids']:
                id = int(id)
                self.get_service().delete(id)
                self.form['error'] = False
                self.form['message'] = "Data has been deleted successfully"

        if request.POST['operation'] == "delete":
            UserListCtl.count = 1
            self.form['page_no'] = UserListCtl.count
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
        return "user_list.html"

    def get_service(self):
        return UserService()
from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Role
from service.service.role_service import RoleService
from ..utility.data_validator import DataValidator


class RoleCtl(BaseCtl):
    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.name = self.form.get("name", "").strip()
        obj.description = self.form.get("description", "").strip()
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.is_null(self.form["name"]):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True
        if DataValidator.is_null(self.form["description"]):
            input_error["description"] = "Description can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        role_id = int(params.get("id", 0))

        if role_id > 0:
            role = self.get_service().get(role_id)
            self.model_to_form(role)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(name=self.form.get('name', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Role already exist"
        else:
            role = self.form_to_model(Role())
            self.get_service().save(role)
            self.form['id'] = role.id
            self.form['error'] = False
            self.form['message'] = "Role added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "role.html"

    def get_service(self):
        return RoleService()

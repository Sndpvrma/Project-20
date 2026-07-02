from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Manager
from service.service.manager_service import ManagerService
from ..utility.data_validator import DataValidator


class ManagerCtl(BaseCtl):
    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["manager_name"] = request_form.get("manager_name", "").strip()
        self.form["branch_name"] = request_form.get("branch_name", "").strip()
        self.form["contact_number"] = request_form.get("contact_number", "").strip()


    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.manager_name = self.form.get("manager_name", "").strip()
        obj.branch_name = self.form.get("branch_name", "").strip()
        obj.contact_number = self.form.get("contact_number", "").strip()

        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["manager_name"] = obj.manager_name
        self.form["branch_name"] = obj.branch_name
        self.form["contact_number"] = obj.contact_number


    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.is_null(self.form["manager_name"]):
            input_error["manager_name"] = "Broker Name can not be null"  # Fixed message
            self.form["error"] = True
        if DataValidator.is_null(self.form["branch_name"]):
            input_error["branch_name"] = "branch_name can not be null"  # Fixed message
            self.form["error"] = True
        if DataValidator.is_null(self.form["contact_number"]):
            input_error["contact_number"] = "Contact Number can not be null"  # Fixed message
            self.form["error"] = True
        elif not DataValidator.is_mobile_number(self.form.get("contact_number")):
            input_error["contact_number"] = "Contact Number must be 10 digits"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        manager_id = int(params.get("id", 0))
        
        if manager_id > 0:
            manager = self.get_service().get(manager_id)
            self.model_to_form(manager)
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(manager_name=self.form.get('manager_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Manager ID already exist"
        else:
            if pk > 0:
                manager_obj = self.get_service().get_model().objects.get(id=pk)
                manager = self.form_to_model(manager_obj)
                manager.id = pk
            else:
                manager = self.form_to_model(Manager())

            self.get_service().save(manager)

            self.form['id'] = str(manager.id)
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Manager updated successfully..!!"
            else:
                self.form['message'] = "Manager added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "manager.html"

    def get_service(self):
        return ManagerService()
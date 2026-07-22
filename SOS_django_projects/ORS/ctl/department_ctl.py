from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Department
from service.service.DepartmentService import DepartmentService
from service.utility.DataValidator import DataValidator


class DepartmentCtl(BaseCtl):

    def preload(self, request):
        return self.preload_data

    # Populate Form from HTTP Request
    def request_to_form(self, request):
        self.form["id"] = request.get("id", 0)
        print('R2F =====================>', self.form["id"])
        self.form["department_id"] = request.get("departmentId", 0)
        self.form["department_name"] = request.get("departmentName", "")
        self.form["hod_name"] = request.get("hodName", "")
        self.form["total_faculty"] = request.get("totalFaculty", "")
        self.form["location"] = request.get("location", "")

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        # print('M2F======================>', self.form["id"])
        self.form["department_id"] = obj.department_id
        self.form["department_name"] = obj.department_name
        self.form["hod_name"] = obj.hod_name
        self.form["total_faculty"] = obj.total_faculty
        self.form["location"] = obj.location
        print('M2F======================>', self.form["location"])


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        print('F2M======================>', obj.id)
        obj.department_id = int(self.form.get("department_id", 0))
        obj.department_name = self.form.get("department_name", "")
        obj.hod_name = self.form.get("hod_name", "")
        obj.total_faculty = self.form.get("total_faculty", "")
        obj.location = self.form.get("location", "")
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["department_id"]):
            inputError["department_id"] = "Department Id is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["department_name"]):
            inputError["department_name"] = "Department Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["hod_name"]):
            inputError["hod_name"] = "HOD Name is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["total_faculty"]):
            inputError["total_faculty"] = "Total Faculty is required"
            self.form["error"] = True
        if DataValidator.isNull(self.form["location"]):
            inputError["location"] = "location is required"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):
        if params["id"] > 0:
            department = self.get_service().get(params["id"])
            self.model_to_form(department)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Submit Role page
    def submit(self, request, _params={}):
        department = self.form_to_model(Department())
        self    .get_service().save(department)
        if int(self.form["id"]) > 0:
            self.form["id"] = department.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    # Template html of Role page
    def get_template(self):
        return "ors/department.html"

    # Service of Role
    def get_service(self):
        return DepartmentService()

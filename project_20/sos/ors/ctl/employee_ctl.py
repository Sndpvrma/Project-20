from .base_ctl import BaseCtl
from django.shortcuts import render
from service.models import Employee
from service.service.employee_service import EmployeeService
from ..utility.data_validator import DataValidator

class EmployeeCtl(BaseCtl):
    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["employee_name"] = request_form.get("employee_name", "").strip()
        self.form["department"] = request_form.get("department", "").strip()
        self.form["salary"] = request_form.get("salary", "").strip()
        self.form["joining_date"] = request_form.get("joining_date", "").strip()

    def form_to_model(self, obj):

        obj.id = 0

        obj.employee_name = self.form.get("employee_name", "")
        obj.department = self.form.get("department", "")
        obj.salary = self.form.get("salary", "")
        obj.joining_date = self.form.get("joining_date", "")

        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["employee_name"] = obj.employee_name
        self.form["department"] = obj.department
        self.form["salary"] = obj.salary
        self.form["joining_date"] = obj.joining_date

    def input_validation(self):

        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.is_null(self.form.get("employee_name")):
            input_error["employee_name"] = "Employee Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("department")):
            input_error["department"] = "Department can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("salary")):
            input_error["salary"] = "Salary Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("joining_date")):
            input_error["joining_date"] = "Joining date can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def preload(self, request):
        pass

    def display(self, request, params={}):
        employee_id = int(params.get("id", 0))

        if employee_id > 0:
            employee = self.get_service().get(employee_id)
            self.model_to_form(employee)
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(employee_name=self.form.get('employee_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Employee ID already exist"
        else:
            if pk > 0:
                employee_obj = self.get_service().get_model().objects.get(id=pk)
                employee = self.form_to_model(employee_obj)
                employee.id = pk
            else:
                employee = self.form_to_model(Employee())

            self.get_service().save(employee)

            self.form['id'] = str(employee.id)
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Employee updated successfully..!!"
            else:
                self.form['message'] = "Employee added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "employee.html"

    def get_service(self):
        return EmployeeService()

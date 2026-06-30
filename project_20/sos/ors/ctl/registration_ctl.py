from datetime import datetime
from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.user_service import UserService
from ..utility.data_validator import DataValidator
from ..utility.html_utility import HtmlUtility
from service.models import User
from service.service.role_service import RoleService
from service.service.email_builder import EmailBuilder
from service.service.email_message import EmailMessage
from service.service.email_service import EmailService

class RegistrationCtl(BaseCtl):

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("first_name", "").strip()
        self.form["last_name"] = request_form.get("last_name", "").strip()
        self.form["login"] = request_form.get("login", "").strip()
        self.form["password"] = request_form.get("password", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["gender"] = request_form.get("gender", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["mobile_number"] = request_form.get("mobile_number", "").strip()
        self.form["role_id"] = request_form.get("role_id", 0)

    def form_to_model(self, obj):

        obj.id = 0

        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.login = self.form.get("login", "")
        obj.password = self.form.get("password", "")

        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.gender = self.form.get("gender", "")
        obj.mobile_number = self.form.get("mobile_number", "")

        role_id = int(self.form.get("role_id") or 0)
        obj.role_id = role_id

        role = RoleService().get(role_id) if role_id > 0 else None
        obj.role_name = role.name if role else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["first_name"] = obj.first_name
        self.form["last_name"] = obj.last_name
        self.form["login"] = obj.login
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["gender"] = obj.gender
        self.form["address"] = obj.address
        self.form["mobile_number"] = obj.mobile_number
        self.form["role_id"] = obj.role_id

    def preload(self, request):
        role_list = RoleService().search({})
        gender_list = ["Male", "Female", "Other"]

        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "role_id",
            int(self.form.get("role_id") or 0),
            role_list
        )

        return self.preload_data

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.is_null(self.form.get("first_name")):
            input_error["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("last_name")):
            input_error["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("login")):
            input_error["login"] = "Login can not be null"
            self.form["error"] = True
        elif not DataValidator.is_email(self.form.get("login")):
            input_error["login"] = "Login must be a valid email address"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("password")):
            input_error["password"] = "Password can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("dob")):
            input_error["dob"] = "DOB can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("address")):
            input_error["address"] = "Address can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("gender")) or self.form.get("gender") == "0":
            input_error["gender"] = "Gender can not be null"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True

        elif not DataValidator.is_mobile_number(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.is_null(self.form.get("role_id")) or self.form.get("role_id") == "0":
            input_error["role_id"] = "Role can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        duplicate = self.get_service().get_model().objects.filter(login=self.form.get('login', ''))

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Login ID already exist"
        else:
            user = self.form_to_model(User())
            self.get_service().save(user)

            self.form['id'] = user.id
            self.form['error'] = False
            self.form['message'] = "User added successfully..!!"

            msg = EmailMessage()
            msg.to = [self.form["login"]]
            msg.subject = "Welcome - Registration Successful"
            msg.text = EmailBuilder.sign_up({"first_name": self.form["first_name"], "login": self.form["login"], "password": self.form["password"]})


            EmailService.send(msg)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "registration.html"

    def get_service(self):
        return UserService()

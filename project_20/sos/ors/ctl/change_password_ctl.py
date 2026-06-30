from django.shortcuts import render
from ..utility.data_validator import DataValidator
from service.service.user_service import UserService
from .base_ctl import BaseCtl
from service.service.email_service import EmailService
from service.service.email_builder import EmailBuilder
from service.service.email_message import EmailMessage
from django.http import HttpResponse


class ChangePasswordCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["old_password"] = requestForm.get("old_password", "")
        self.form["new_password"] = requestForm.get("new_password", "")
        self.form["confirm_password"] = requestForm.get("confirm_password", "")

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]
        if DataValidator.is_null(self.form.get("old_password")):
            input_error["old_password"] = "Old Password cannot be null"
            self.form["error"] = True
        if DataValidator.is_null(self.form.get("new_password")):
            input_error["new_password"] = "New Password cannot be null"
            self.form["error"] = True
        if DataValidator.is_null(self.form.get("confirm_password")):
            input_error["confirm_password"] = "Confirm Password cannot be null"
            self.form["error"] = True
        elif self.form.get("new_password") != self.form.get("confirm_password"):
            input_error["confirm_password"] = "New Password and Confirm Password do not match"
            self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        login_id = request.session.get("login_id")
        user = self.get_service().get(login_id)
        if user is None:
            self.form["error"] = True
            self.form["message"] = "Session expired. Please login again."
            return render(request, self.get_template(), {"form": self.form})
        if user.password != self.form.get("old_password"):
            self.form["input_error"]["old_password"] = "Old Password is incorrect"
            self.form["error"] = True
            return render(request, self.get_template(), {"form": self.form})
        user.password = self.form.get("new_password")
        self.get_service().save(user)
        self.form["error"] = False
        self.form["message"] = "Password changed successfully"
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password(
            {"first_name": user.first_name, "login": user.login, "password": self.form.get("new_password")})
        EmailService.send(msg)

        return render(request, self.get_template(), {"form": self.form})

    def get_template(self):
        return "change_password.html"

    def get_service(self):
        return UserService()

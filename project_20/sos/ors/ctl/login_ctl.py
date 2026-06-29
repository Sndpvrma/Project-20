from django.shortcuts import render, redirect
from service.service.user_service import UserService
from .base_ctl import BaseCtl
from ..utility.data_validator import DataValidator

class LoginCtl(BaseCtl):
    def request_to_form(self, requestFrom):
        self.form["login"] = requestFrom["login"]
        self.form["password"] = requestFrom["password"]
        self.form["remember_me"] = requestFrom.get("remember_me", False)

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]
        if DataValidator.is_null(self.form.get("login")):
            input_error["login"] = "Login can not be null"
            self.form["error"] = True
        if DataValidator.is_null(self.form.get("password")):
            input_error["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        # if request.session.get("loginId"):
        #     return redirect('/ORS/Welcome')
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        user = self.get_service().authenticate(self.form)
        if (user is None):
            self.form["error"] = True
            self.form["message"] = "Invalid Login or Password"
            res = render(request, self.get_template(), {"form": self.form})
        else:
            if self.form.get("rememberMe"):
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # expires when browser closes
            request.session["user_id"] = user.id
            request.session["login_id"] = user.login
            request.session["first_name"] = user.first_name
            request.session["last_name"] = user.last_name
            res = redirect('/dm/welcome')
        return res

    def get_template(self):
        return "login.html"

    def get_service(self):
        return UserService()


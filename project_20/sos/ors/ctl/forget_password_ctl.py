from django.shortcuts import render
from ..utility.data_validator import DataValidator
from service.service.forget_password_service import ForgetPasswordService
from service.service.email_service import EmailService
from service.service.email_builder import EmailBuilder
from service.service.email_message import EmailMessage
from .base_ctl import BaseCtl

class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self,requestFrom):
        self.form["login_id"] = requestFrom.get("login_id", "")

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]
        if DataValidator.is_null(self.form.get("login_id")):
            input_error["login_id"] = "Login can not be null"
            self.form["error"] = True
        return self.form["error"]

    def display(self,request,params={}):
        return render(request,self.get_template(),{"form":self.form})

    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        if(self.input_validation()):
            return render(request,self.get_template(),{"form":self.form})
        else:
            user_qs = self.get_service().search(self.form)
            if(user_qs.count() == 0):
                self.form["message"] = "Invalid ID"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                user = user_qs[0]
                # request.session["user"] = user.login
                msg = EmailMessage()
                msg.to = [user.login]
                msg.subject = "Forgot Password Request"
                msg.text = EmailBuilder.forgot_password({"first_name": user.first_name, "login": user.login, "password": user.password})
                EmailService.send(msg)
                self.form["message"] = "Password reset email has been sent"
                res = render(request,self.get_template(),{"form":self.form})
        return res

    def get_template(self):
        return "forget_password.html"

    def get_service(self):
        return ForgetPasswordService()        


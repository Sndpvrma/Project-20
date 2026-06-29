from .base_ctl import BaseCtl
from django.shortcuts import render


class WelcomeCtl(BaseCtl):

    def display(self, request, params={}):
        user_login = request.session.get("user", None)
        if (user_login is not None):
            self.form["message"] = "Welcome " + user_login
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    def get_service(self):
        pass

    def get_template(self):
        return "welcome.html"

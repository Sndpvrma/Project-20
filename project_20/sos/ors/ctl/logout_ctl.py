from .base_ctl import BaseCtl
from django.shortcuts import redirect


class LogoutCtl(BaseCtl):

    def display(self, request, _params={}):
        request.session.flush()
        return redirect('/ors/Login')

    def submit(self, request, _params={}):
        request.session.flush()
        return redirect('/ors/Login')

    def get_template(self):
        return "login.html"

    def get_service(self):
        pass
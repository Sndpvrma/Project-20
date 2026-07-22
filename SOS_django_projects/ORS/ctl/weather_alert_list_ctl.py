from django.shortcuts import render, redirect

from service.service.WeatherAlertService import WeatherAlertService
from .BaseCtl import BaseCtl



class WeatherAlertListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['alert_id'] = requestForm.get('alertId')

    def display(self, request, params={}):
        alert_list = self.get_service().search(self.form)
        self.form['list'] = alert_list
        return render(request, self.get_template(), {'form': self.form})

    def submit(self, request, params={}):

        if request.POST.get('operation', '') == "next":
            self.form['page_number'] = int(request.POST['pageNumber'])
            self.form['page_number'] += 1
        if request.POST.get('operation', '') == "previous":
            self.form['page_number'] = int(request.POST['pageNumber'])
            self.form['page_number'] -= 1
        if request.POST.get('operation', '') == "search":
            self.form['page_number'] = 1

        alert_list = self.get_service().search(self.form)
        self.form['list'] = alert_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return WeatherAlertService()

    def get_template(self):
        return 'ors/weatheralertlist.html'
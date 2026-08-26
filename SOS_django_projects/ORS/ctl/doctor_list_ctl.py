from django.shortcuts import render, redirect

from service.service.DoctorService import DoctorService
from .BaseCtl import BaseCtl



class DoctorListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['doctor_id'] = requestForm.get('doctorId')

    def display(self, request, params={}):
        doctor_list = self.get_service().search(self.form)
        self.form['list'] = doctor_list
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

        doctor_list = self.get_service().search(self.form)
        self.form['list'] = doctor_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return DoctorService()

    def get_template(self):
        return 'ors/doctorlist.html'
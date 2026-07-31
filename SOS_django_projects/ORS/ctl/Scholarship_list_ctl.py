from django.shortcuts import render, redirect

from service.service.ScholarshipService import ScholarshipService
from .BaseCtl import BaseCtl



class ScholarshipListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['scholarship_id'] = requestForm.get('scholarshipId')

    def display(self, request, params={}):
        scholarship_list = self.get_service().search(self.form)
        self.form['list'] = scholarship_list
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

        drone_list = self.get_service().search(self.form)
        self.form['list'] = drone_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return ScholarshipService()

    def get_template(self):
        return 'ors/scholarshipList.html'
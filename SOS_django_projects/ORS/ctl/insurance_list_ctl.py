from django.shortcuts import render, redirect

from service.service.InsuranceService import InsuranceService
from .BaseCtl import BaseCtl



class InsuranceListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['policy_id'] = requestForm.get('policyId')

    def display(self, request, params={}):
        insurance_list = self.get_service().search(self.form)
        self.form['list'] = insurance_list
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

        insurance_list = self.get_service().search(self.form)
        self.form['list'] = insurance_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return InsuranceService()

    def get_template(self):
        return 'ors/insuranceList.html'
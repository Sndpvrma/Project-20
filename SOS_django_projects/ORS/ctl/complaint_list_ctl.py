from django.shortcuts import render, redirect

from service.service.ComplaintService import ComplaintService
from .BaseCtl import BaseCtl



class ComplaintListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['complaint_id'] = requestForm.get('complaintId')

    def display(self, request, params={}):
        complaint_list = self.get_service().search(self.form)
        self.form['list'] = complaint_list
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

        complaint_list = self.get_service().search(self.form)
        self.form['list'] = complaint_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return ComplaintService()

    def get_template(self):
        return 'ors/complaintlist.html'
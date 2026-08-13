from django.shortcuts import render, redirect

from service.service.VendorService import VendorService
from .BaseCtl import BaseCtl



class VendorListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['vendor_id'] = requestForm.get('vendorId')

    def display(self, request, params={}):
        vendor_list = self.get_service().search(self.form)
        self.form['list'] = vendor_list
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

        vendor_list = self.get_service().search(self.form)
        self.form['list'] = vendor_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return VendorService()

    def get_template(self):
        return 'ors/vendorlist.html'
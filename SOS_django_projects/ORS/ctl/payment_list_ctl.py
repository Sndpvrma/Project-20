from django.shortcuts import render, redirect

from service.service.PaymentService import PaymentService
from .BaseCtl import BaseCtl



class PaymentListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['payment_id'] = requestForm.get('paymentId')

    def display(self, request, params={}):
        payment_list = self.get_service().search(self.form)
        self.form['list'] = payment_list
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

        payment_list = self.get_service().search(self.form)
        self.form['list'] = payment_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return PaymentService()

    def get_template(self):
        return 'ors/paymentlist.html'
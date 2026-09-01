from django.shortcuts import render, redirect

from service.service.BankAccountService import BankAccountService
from .BaseCtl import BaseCtl



class BankAccountListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['account_number'] = requestForm.get('accountNumber')

    def display(self, request, params={}):
        bank_account_list = self.get_service().search(self.form)
        self.form['list'] = bank_account_list
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

        bank_account_list = self.get_service().search(self.form)
        self.form['list'] = bank_account_list
        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return BankAccountService()

    def get_template(self):
        return 'ors/bankaccountlist.html'
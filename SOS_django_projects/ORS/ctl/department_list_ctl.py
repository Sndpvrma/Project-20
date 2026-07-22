from django.shortcuts import render, redirect

from service.service.DepartmentService import DepartmentService
from .BaseCtl import BaseCtl



class DepartmentListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['department_id'] = requestForm.get('departmentId')

    def display(self, request, params={}):
        drone_list = self.get_service().search(self.form)
        self.form['list'] = drone_list
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
        return DepartmentService()

    def get_template(self):
        return 'ors/departmentList.html'
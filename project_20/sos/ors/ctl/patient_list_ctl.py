from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.patient_service import PatientService

class PatientListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["patient_name"] = request_form.get("patient_name", "").strip()
        self.form["disease"] = request_form.get("disease", "").strip()
        self.form["doctor_name"] = request_form.get("doctor_name", "").strip()
        self.form["age"] = request_form.get("age", " ").strip()
        self.form['ids'] = request_form.getlist('ids', None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = PatientListCtl.count

        if request.POST['operation'] == "next":
            PatientListCtl.count += 1
            self.form['page_no'] = PatientListCtl.count
        if request.POST['operation'] == "previous":
            PatientListCtl.count -= 1
            self.form['page_no'] = PatientListCtl.count
        if request.POST['operation'] == "search":
            PatientListCtl.count = 1
            self.form['page_no'] = PatientListCtl.count
        if request.POST['operation'] == "delete":
            PatientListCtl.count = 1
            self.form['page_no'] = PatientListCtl.count
            for id in self.form['ids']:
                id = int(id)
                self.get_service().delete(id)
                self.form['error'] = False
                self.form['message'] = "Data has been deleted successfully"

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "patient_list.html"

    def get_service(self):
        return PatientService()
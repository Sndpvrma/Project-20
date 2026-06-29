from django.shortcuts import render
from .base_ctl import BaseCtl
from service.service.broker_service import BrokerService

class BrokerListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["broker_name"] = request_form.get("broker_name", "").strip()
        self.form["contact_number"] = request_form.get("contact_number", "").strip()
        self.form["company"] = request_form.get("company", "").strip()
        self.form['ids'] = request_form.getlist('ids', None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):
        self.form['page_no'] = BrokerListCtl.count

        if request.POST['operation'] == "next":
            BrokerListCtl.count += 1
            self.form['page_no'] = BrokerListCtl.count
        if request.POST['operation'] == "previous":
            BrokerListCtl.count -= 1
            self.form['page_no'] = BrokerListCtl.count
        if request.POST['operation'] == "search":
            BrokerListCtl.count = 1
            self.form['page_no'] = BrokerListCtl.count
        if request.POST['operation'] == "delete":
            BrokerListCtl.count = 1
            self.form['page_no'] = BrokerListCtl.count
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
        return "broker_list.html"

    def get_service(self):
        return BrokerService()